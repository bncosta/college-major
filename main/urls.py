from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url
from main.views import collegeMajor, MajorAutoComplete, SchoolAutoComplete


from . import views

"""
'major-autocomplete' and 'university-autocomplete' needs to be implemented more securely
"""
urlpatterns = [
    path('', collegeMajor.as_view(), name='index'),
    url(
        r'^major-autocomplete/$',
        MajorAutoComplete.as_view(),
        name='major-autocomplete',
    ),
    url(
        r'^school-autocomplete/$',
        SchoolAutoComplete.as_view(),
        name='school-autocomplete',
    ),
]
