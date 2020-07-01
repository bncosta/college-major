from django.shortcuts import render
from main.models import Collegemajor
from collections import defaultdict
from django.db import connection
from django.views.generic import TemplateView
from main.forms import MajorForm, SchoolForm
from dal import autocomplete

"""
- Used for Index.html page
- Allows users to search majors by earnings & universities
"""


class CollegeMajor(TemplateView):
    mForm = MajorForm
    sForm = SchoolForm

    # gets context data that will always be rendered
    def get_context_data(self, request, **context):
        # NOT IMPLEMENTED PROPERLY! Forms to assist in autocomplete
        context['MajorForm'] = self.mForm()
        context['SchoolForm'] = self.sForm()
        return super(CollegeMajor, self).get_context_data(**context)

    # called for index.html
    def get(self, request):
        # dictionary of key:value pairs sent to front end
        context = self.get_context_data(request)

        # display schools that pay the highest for a given major to front-end
        if "major" in request.GET.keys():
            major = request.GET['major'].lower()
            schools_with_major = schools_query(major)
            # context['schools'], context['uni_names_pub'], context['uni_names_priv_np'], \
            # context['uni_names_priv_fp'], context['coordinate_points_pub'], context['coordinate_points_priv_np'], \
            # context['coordinate_points_priv_fp'] = highest_major(major, schools_with_major)
            highest_universities, uni_names, coordinate_points = highest_major(major, schools_with_major)

            # gets the median salary for masters degree, given the bachelor degree inputted
            context['median_masters'] = get_median_masters(major)

            # front end will use this value to check if graduate data available
            if context['median_masters'] != dict():
                context['median_masters']['has_values'] = True
            else:
                context['median_masters']['has_values'] = False

            # retrieves highest universities
            context['schools'] = highest_universities

            # Retrieves university names & catagorizes them based on their school type
            context['uni_names_pub'] = uni_names["Public"]
            context['uni_names_priv_np'] = uni_names["Private, nonprofit"]
            context['uni_names_priv_fp'] = uni_names["Private, for-profit"]

            # Retrieves coordinate points & catagorizes them based on their school type
            context['coordinate_points_pub'] = coordinate_points["Public"]
            context['coordinate_points_priv_np'] = coordinate_points["Private, nonprofit"]
            context['coordinate_points_priv_fp'] = coordinate_points["Private, for-profit"]

            # retrieves 5 number summary of data
            context['boxplot'] = {"big_5": get_five_number_summary(schools_with_major)}
            context['major'] = major.title()

            # gets average first year salary of major across all schools
            context['average_salary'] = average_salary(highest_universities)

        # display top paying majors for a given university to front-end
        if "school" in request.GET.keys():
            school = request.GET['school'].lower()
            context['majors'], context["major_names"], context["coordinate_points"] = highest_school(school)

        if "highest_avg" in request.GET.keys():
            context['majors'], context["major_names"], context["coordinate_points"] = highest_avg_major()

        # gets all_major_stats: hardcoded values for 1st quartile, median, and 3rd quartile for all majors
        context['all_major_stats'] = all_major_stats()

        # returns output
        return render(request, "index.html", context)

    # # TESTING PHASE interprets form data
    # def post(self, request):
    #     majors = self.mForm(request.POST)
    #     if not majors.is_valid():
    #         print(majors.cleaned_data['cipdesc'])
    #     return render(request, "index.html")


class MajorAutoComplete(autocomplete.Select2QuerySetView):
    # code that enables autocomplete search for majors
    def get_queryset(self):
        # gets dataset of majors
        majors = Collegemajor.objects.filter(credlev='5').values_list('cipdesc').distinct()

        # filters user search by major
        if self.q:
            majors = majors.filter(cipdesc__icontains=self.q)

        return majors

    # Because we are only unpacking a list of majors, we simply return the string of the tuple instead of pk obj
    # (pk objects help organize serialized data)
    def get_result_value(self, result):
        result = result[0].title()
        return result

    # formats text correctly on front-end
    def get_result_label(self, result):
        result = result[0].title()
        return result


class SchoolAutoComplete(autocomplete.Select2QuerySetView):
    # code that enables autocomplete search for schools
    def get_queryset(self):
        # gets dataset of school
        schools = Collegemajor.objects.filter(credlev='5').values_list('instnm').distinct()

        # filters user search by school
        if self.q:
            schools = schools.filter(instnm__icontains=self.q)

        return schools

    # Because we are only unpacking a list of schools, we simply return the string of the tuple instead of pk obj
    # (pk objects help organize serialized data)
    def get_result_value(self, result):
        return result

    # formats text correctly on front-end
    def get_result_label(self, result):
        result = result[0].title()
        return result


"""
Helper Methods - (Could possibly be reimplemented in class?)
"""


# returns dictionary of universities that pay the highest for
def highest_major(major, university_list):
    if major is None or "":
        return None

    # universities that receive highest pay from major
    highest_universities = defaultdict(dict)

    # names of universities, categorized by private / public
    uni_names = {"Private, nonprofit": [], "Public": [], "Private, for-profit": []}

    # list of data points that will be passed to front end
    coordinate_points = {"Private, nonprofit": [], "Public": [], "Private, for-profit": []}

    for m in university_list:
        highest_universities[m.instnm]["median_earnings"] = m.md_earn_wne
        coords = {'x': m.md_earn_wne, 'y': m.debtmedian}

        if coords['y'] != 'PrivacySuppressed':
            if m.control == "Private, nonprofit":
                coordinate_points["Private, nonprofit"].append(coords)
                uni_names["Private, nonprofit"].append(m.instnm.title())

            elif m.control == "Public":
                coordinate_points["Public"].append(coords)
                uni_names["Public"].append(m.instnm.title())

            elif m.control == "Private, for-profit":
                coordinate_points["Private, for-profit"].append(coords)
                uni_names["Private, for-profit"].append(m.instnm.title())

    # returns dictionaries
    return dict(highest_universities), uni_names, coordinate_points


# returns average salary of major across all schools
def average_salary(highest_universities):
    # gets the average pay for this major across all universities
    salaries = [int(v["median_earnings"]) for v in list(highest_universities.values())]
    return int(round(sum(salaries) / len(salaries), -2))


# returns list of schools which have pay data for the given major
def schools_query(major):
    if major is None or "":
        return None
    major = major.replace("'", "''")
    major = major.replace('"', '""')
    query1 = f"SELECT * FROM collegemajor WHERE cipdesc = '{major}' " \
             f"and credlev = '5' order by md_earn_wne::int desc;"
    return Collegemajor.objects.raw(query1)


# returns dictionary of majors that pay the highest for a given school
def highest_school(school):
    # majors that receive highest pay in school
    highest_majors = defaultdict(dict)

    # if major is valid, then pulls top 10 highest paying schools
    if school is not None:
        # if the school name has a single or double quote (ie: Saint Mary's),
        # replace it with two single or double quotes. This is equivalent to escape sequencing for PostGreSql
        school = school.replace("'", "''")
        school = school.replace('"', '""')
        query1 = f"SELECT id, cipdesc, md_earn_wne, debtmedian FROM collegemajor WHERE instnm = '{school}' " \
                 f"and credlev = '5' order by md_earn_wne::int desc;"

        # names of majors that the university teaches
        major_names = []

        # data points that will be passed to front-end
        coordinate_points = []
        for m in Collegemajor.objects.raw(query1):
            highest_majors[m.cipdesc]["median_earnings"] = m.md_earn_wne
            highest_majors[m.cipdesc]["median_debt"] = m.debtmedian
            coords = {'x': m.md_earn_wne, 'y': m.debtmedian}
            major_names.append(m.cipdesc.title())
            coordinate_points.append(coords)

        # returns dictionary
        return dict(highest_majors), major_names, coordinate_points


# returns dictionary of majors by average starting salary across all universities
def highest_avg_major():
    # majors that receive highest pay in school
    highest_majors = defaultdict(dict)

    with connection.cursor() as cursor:
        # if major is valid, then pulls top 10 highest paying schools
        query1 = f"SELECT AVG(NULLIF(md_earn_wne, '')::int) as average_earnings, " \
                 f"AVG(NULLIF(debtmedian, 'PrivacySuppressed')::int) as average_debt, cipdesc  FROM collegemajor " \
                 f"WHERE credlev = '5' group by cipdesc order by average_earnings desc;"

        cursor.execute(query1)

        # # Useful to find median, and quartiles wages for entire dataset.
        # query2 = f"SELECT md_earn_wne, id FROM collegemajor " \
        #          f"WHERE credlev = '3' order by md_earn_wne desc;"
        # cursor.execute(query2)
        # import statistics
        # values = []
        #
        # for md_earn_wne in cursor.fetchall():
        #     values.append(int(md_earn_wne[0]))
        # values.sort()
        #
        # print(statistics.median(values[10695:-1]))

        major_names = list()
        coordinate_points = list()
        for avg_salary, median_debt, major_name in cursor.fetchall():
            # note average_debt may be none if there is debt data available for any of the schools that had the major
            if median_debt is not None:

                # averages will be decimals, too specific and not accurate to be a float given significant figures
                avg_salary = int(round(avg_salary, -2))
                median_debt = int(round(median_debt, -2))
                highest_majors[major_name]["median_earnings"] = avg_salary
                highest_majors[major_name]["median_debt"] = median_debt
                coords = {'x': avg_salary, 'y': median_debt}
                major_names.append(major_name.title())
                coordinate_points.append(coords)

        # returns dictionary
        return dict(highest_majors), major_names, coordinate_points


# returns min, Q1, median, Q3, and maximum pay of universities for a given majors
def get_five_number_summary(universities):
    return {
        'max': universities[0].md_earn_wne,
        'q3': universities[int(len(universities)/4)].md_earn_wne,
        'med': universities[int(len(universities)/2)].md_earn_wne,
        'q1': universities[int(len(universities)/4 + len(universities)/2)].md_earn_wne,
        'min': universities[int(len(universities)-1)].md_earn_wne
    }


# returns min, Q1, median, Q3, and maximum pay of universities for a given majors for a sorted
# list of ints
def get_five_number_summary_sorted_list(universities: [int]) -> dict:
    return {
        'max': universities[0],
        'q3': universities[int(len(universities)/4)],
        'med': universities[int(len(universities)/2)],
        'q1': universities[int(len(universities)/4 + len(universities)/2)],
        'min': universities[int(len(universities)-1)]
    }


# hardcoded values for 1st quartile, median, and 3rd quartile for all majors (bachelor's)
def all_major_stats():
    FIRST_QUARTILE = 28400
    MEDIAN = 34500
    SECOND_QUARTILE = 45300

    return {'q1': FIRST_QUARTILE, 'median': MEDIAN, 'q3': SECOND_QUARTILE}


def get_median_masters(major: str):
    with connection.cursor() as cursor:
        print(major)
        query1 = f"SELECT md_earn_wne FROM collegemajor WHERE cipdesc = '{major}' and credlev = '5';"
        cursor.execute(query1)

        graduate_values = []

        for md_earn_wne in cursor.fetchall():
            graduate_values.append(int(md_earn_wne[0]))

        # print(get_five_number_summary_sorted_list(sorted(graduate_values, reverse=True)))

        if len(graduate_values) != 0:
            return get_five_number_summary_sorted_list(sorted(graduate_values, reverse=True))
        else:
            return dict()

