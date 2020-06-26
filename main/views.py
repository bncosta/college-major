# from django.http import HttpResponse, HttpResponseRedirect
import decimal

from django.shortcuts import render
from main.models import Collegemajor
from collections import defaultdict
from django.db import connection
from django.views.generic import TemplateView
from django.views.generic import FormView
from main.forms import MajorForm, SchoolForm
from dal import autocomplete

"""
- Used for Index.html page
- Allows users to search majors by price & universities
"""
class collegeMajor(TemplateView):
    mForm = MajorForm
    sForm = SchoolForm

    # gets context data that will always be rendered
    def get_context_data(self, request, **context):
        # NOT IMPLEMENTED PROPERLY! Forms to assist in autocomplete
        context['MajorForm'] = self.mForm()
        context['SchoolFrom'] = self.sForm()
        return super(collegeMajor, self).get_context_data(**context)

    # called for index.html
    def get (self, request):
        # dictionary of key:value pairs sent to front end
        context = {}
        context = self.get_context_data(request)

        # display schools that pay the highest for a given major to front-end
        if "major" in request.GET.keys():
            major = request.GET['major'].lower()
            context['schools'], context['average_salary'] = highest_major(major)

        # display top paying majors for a given university to front-end
        if "school" in request.GET.keys():
            school = request.GET['school'].lower()
            context['majors'] = highest_school(school)

        if "highest_avg" in request.GET.keys():
            context['majors'] = highest_avg_major()

        # returns output
        return render(request, "index.html", context)

    # TESTING PHASE interprets form data
    def post(self, request):
        majors = self.mForm(request.POST)
        if majors.is_valid():
            print('yay, it works!')
        else:
            print('Rats!')
            print(majors.cleaned_data['cipdesc'])
        return render(request, "index.html")

"""
(NEEDS TO BE IMPLEMENTED MORE SECURELY) used to display autocomplete results for majors
"""
class majorAutoComplete(autocomplete.Select2QuerySetView):
    # code that enables autocomplete search for majors
    def get_queryset(self):
        # gets dataset of majors
        majors = Collegemajor.objects.values_list('cipdesc').distinct()

        #filters user search by major
        if self.q:
            majors = majors.filter(cipdesc__istartswith = self.q)

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

"""
(NEEDS TO BE IMPLEMENTED MORE SECURELY) used to display autocomplete results for schools
"""
class schoolAutoComplete(autocomplete.Select2QuerySetView):
    # code that enables autocomplete search for schools
    def get_queryset(self):
        # gets dataset of school
        schools = Collegemajor.objects.values_list('instnm').distinct()

        #filters user search by school
        if self.q:
            schools = schools.filter(instnm__istartswith = self.q)

        return schools

    # Because we are only unpacking a litst of schools, we simply return the string of the tuple instead of pk obj
    # (pk objects help organize serialized data)
    def get_result_value(self, result):
        return result

"""
Helper Methods - (Could possibly be reimplemented in class?)
"""
# returns dictionary of universities that pay the highest for a given major
def highest_major(major):
    # universities that receive highest pay from major
    highest_universities = defaultdict(dict)

    # if major is valid, then pulls top 10 highest paying schools
    if major is not None:
        query1 = f"SELECT * FROM collegemajor WHERE cipdesc = '{major}' " \
                 f"and credlev = '3' order by md_earn_wne::int desc;"

        for m in Collegemajor.objects.raw(query1):
            highest_universities[m.instnm]["median_earnings"] = m.md_earn_wne

        avg_salary = None

        # make sure results were returned for this major
        if len(highest_universities) != 0:
            with connection.cursor() as cursor:
                query2 = f"SELECT AVG(NULLIF(md_earn_wne, '')::int)  FROM collegemajor " \
                         f"WHERE cipdesc = '{major}' and credlev = '3';"
                cursor.execute(query2)
                avg_salary = round(cursor.fetchone()[0], -2)
    # returns dictionary
    return dict(highest_universities), avg_salary


# returns dictionary of majors that pay the highest for a given school
def highest_school(school):
    # majors that receive highest pay in school
    highest_majors = defaultdict(dict)

    # if major is valid, then pulls top 10 highest paying schools
    if school is not None:
        query1 = f"SELECT * FROM collegemajor WHERE instnm = '{school}' " \
                 f"and credlev = '3' order by md_earn_wne::int desc;"
        for m in Collegemajor.objects.raw(query1):

            highest_majors[m.cipdesc]["median_earnings"] = m.md_earn_wne

    # returns dictionary
        return dict(highest_majors)

# returns dictionary of majors by average starting salary
def highest_avg_major():
    # majors that receive highest pay in school
    highest_majors = defaultdict(dict)

    with connection.cursor() as cursor:
        # if major is valid, then pulls top 10 highest paying schools
        query1 = f"SELECT AVG(NULLIF(md_earn_wne, '')::int) as average, cipdesc  FROM collegemajor " \
                 f"WHERE credlev = '3' group by cipdesc order by average desc;"
        print(query1)

        cursor.execute(query1)
        for avg_salary, major_name in cursor.fetchall():
            avg_salary = round(avg_salary, -2)
            highest_majors[major_name]["median_earnings"] = avg_salary

    # returns dictionary
        return dict(highest_majors)

