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
            context['schools'], context['average_salary'], context['uni_names_pub'], context['uni_names_priv_np'], \
            context['uni_names_priv_fp'], context['coordinate_points_pub'], context['coordinate_points_priv_np'], \
            context['coordinate_points_priv_fp'] = highest_major(major)

            context['major'] = major.title()

        # display top paying majors for a given university to front-end
        if "school" in request.GET.keys():
            school = request.GET['school'].lower()
            context['majors'], context["major_names"], context["coordinate_points"] = highest_school(school)

        if "highest_avg" in request.GET.keys():
            context['majors'], context["major_names"], context["coordinate_points"] = highest_avg_major()

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
        majors = Collegemajor.objects.filter(credlev='3').values_list('cipdesc').distinct()

        # filters user search by major
        if self.q:
            majors = majors.filter(cipdesc__icontains=self.q)

        print(type(majors))
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
        schools = Collegemajor.objects.filter(credlev='3').values_list('instnm').distinct()

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


# returns dictionary of universities that pay the highest for a given major
def highest_major(major):
    print(major)
    if major is None or "":
        return None

    # universities that receive highest pay from major
    highest_universities = defaultdict(dict)

    major = major.replace("'", "''")
    major = major.replace('"', '""')
    query1 = f"SELECT * FROM collegemajor WHERE cipdesc = '{major}' " \
             f"and credlev = '3' order by md_earn_wne::int desc;"

    # names of universities, categorized by private / public
    uni_names = {"Private, nonprofit": [], "Public": [], "Private, for-profit": []}

    # list of data points that will be passed to front end
    coordinate_points = {"Private, nonprofit": [], "Public": [], "Private, for-profit": []}

    for m in Collegemajor.objects.raw(query1):
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

    avg_salary = None

    # first makes sure there are results for this major (user didnt input non existent major)
    # next, gets the average pay for this major across all universities
    if len(highest_universities) != 0:
        with connection.cursor() as cursor:
            query2 = f"SELECT AVG(NULLIF(md_earn_wne, '')::int)  FROM collegemajor WHERE cipdesc = '{major}' " \
                     f"and credlev = '3';"
            cursor.execute(query2)
            avg_salary = int(round(cursor.fetchone()[0], -2))

    # returns dictionary
    return dict(highest_universities), avg_salary, uni_names["Public"], uni_names["Private, nonprofit"], \
           uni_names["Private, for-profit"], coordinate_points["Public"], coordinate_points["Private, nonprofit"], \
           coordinate_points["Private, for-profit"]


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
                 f"and credlev = '3' order by md_earn_wne::int desc;"

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
                 f"WHERE credlev = '3' group by cipdesc order by average_earnings desc;"

        cursor.execute(query1)
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
