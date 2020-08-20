from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url
from main.views import CollegeMajor, MajorAutoComplete, SchoolAutoComplete, TitleView
from main.views_masters import CollegeMajor as CollegeMajorMasters,\
    MajorAutoComplete as MajorAutoCompleteMasters, SchoolAutoComplete as SchoolAutoCompleteMasters


from . import views

"""
'main' is going to be the title page
"""
urlpatterns = [
    path('', CollegeMajor.as_view(), name='index'),
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
    path('masters', CollegeMajorMasters.as_view(), name='masters'),
    url(
        r'^major-autocomplete-masters/$',
        MajorAutoCompleteMasters.as_view(),
        name='major-autocomplete-masters',
    ),
    url(
        r'^school-autocomplete-masters/$',
        SchoolAutoCompleteMasters.as_view(),
        name='school-autocomplete-masters',
    ),
    path('title-page', TitleView.as_view(), name = 'title-page')
]
