# from django.http import HttpResponse, HttpResponseRedirect
import decimal

from django.shortcuts import render
from main.models import Collegemajor
from collections import defaultdict
from django.db import connection


# called for index.html
def index(request):
    # dictionary of key:value pairs sent to front end
    context = {}

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

        cursor.execute(query1)
        for avg_salary, major_name in cursor.fetchall():
            avg_salary = round(avg_salary, -2)
            highest_majors[major_name]["median_earnings"] = avg_salary

    # returns dictionary
        return dict(highest_majors)

