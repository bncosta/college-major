from dal import autocomplete
from django import forms
from main.models import Collegemajor

"""
Form that assist in autocomplete for major selection
"""
class MajorForm(forms.ModelForm):
    major = forms.ModelChoiceField(
        #only searches for majors
        queryset=Collegemajor.objects.values_list('cipdesc'),
        widget = autocomplete.ModelSelect2(url = 'major-autocomplete',)
    )
    class Meta:
        model = Collegemajor
        fields = ('cipdesc',)

"""
Form that assist in autocomplete for school selection
"""
class SchoolForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        #only searches for majors
        queryset=Collegemajor.objects.values_list('instnm'),
        widget = autocomplete.ModelSelect2(url = 'school-autocomplete',)
    )
    class Meta:
        model = Collegemajor
        fields = ('instnm',)