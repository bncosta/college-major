from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url
from main.views import collegeMajor, majorAutoComplete, schoolAutoComplete


from . import views

"""
'major-autocomplete' and 'university-autocomplete' needs to be implemented more securely
"""
urlpatterns = [
    path('', collegeMajor.as_view(), name='index'),
    url(
        r'^major-autocomplete/$',
        majorAutoComplete.as_view(),
        name='major-autocomplete',
    ),
    url(
        r'^school-autocomplete/$',
        schoolAutoComplete.as_view(),
        name='school-autocomplete',
    ),
]
