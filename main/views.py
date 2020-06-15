# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import Collegemajor
from collections import defaultdict


# called for index.html
def index(request):
    # dictionary of key:value pairs sent to front end
    context = {}

    # display schools that pay the highest for a given major to front-end
    major = None
    if "major" in request.GET.keys():
        major = request.GET['major'].lower()
        context['schools'] = highest_major(major)

    # display top paying majors for a given university to front-end
    school = None
    if "school" in request.GET.keys():
        major = request.GET['school'].lower()
        context['majors'] = highest_school(major)

    #returns output
    return render(request, "index.html", context)

# returns dictionary of universities that pay the highest for a given major
def highest_major(major):
    # universities that recieve highest pay from major
    highest_universities = defaultdict(dict)

    # if major is valid, then pulls top 10 highest paying schools
    if major is not None:
        query1 = f"SELECT * FROM collegemajor WHERE cipdesc = '{major}' " \
                 f"and credlev = '3' order by md_earn_wne::int desc LIMIT 10;"
        for m in Collegemajor.objects.raw(query1):
            highest_universities[m.instnm]["median_earnings"] = m.md_earn_wne

    #returns dictionary
    return dict(highest_universities)

# returns dictionary of majors that pay the highest for a given school
def highest_school(school):
    # majors that recieve highest pay in school
    highest_majors = defaultdict(dict)

    # if major is valid, then pulls top 10 highest paying schools
    if school is not None:
        query1 = f"SELECT * FROM collegemajor WHERE instnm = '{school}' " \
                 f"and credlev = '3' order by md_earn_wne::int desc LIMIT 10;"
        for m in Collegemajor.objects.raw(query1):

            highest_majors[m.cipdesc]["median_earnings"] = m.md_earn_wne

    #returns dictionary
        return dict(highest_majors)
