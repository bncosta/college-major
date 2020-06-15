# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import Collegemajor
from collections import defaultdict


# called for index.html
def index(request):
    # dictionary of key:value pairs sent to front end
    context = {}
    universities = defaultdict(dict)
    major = None
    if "major" in request.GET.keys():
        major = request.GET['major'].lower()

    if major is not None:
        query1 = f"SELECT * FROM collegemajor WHERE cipdesc = '{major}' " \
                 f"and credlev = '3' order by md_earn_wne::int desc LIMIT 10;"
        for m in Collegemajor.objects.raw(query1):
            universities[m.instnm]["median_earnings"] = m.md_earn_wne

    context['universities'] = dict(universities)
    print(universities)
    return render(request, "index.html", context)
