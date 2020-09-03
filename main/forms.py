from dal import autocomplete
from django import forms
from main.models import Collegemajor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField
"""
Form that assist in autocomplete for major selection
"""


class MajorForm(forms.ModelForm):
    major = forms.ModelChoiceField(
        # only searches for majors
        queryset=Collegemajor.objects.values_list('cipdesc'),
        widget=autocomplete.ModelSelect2(url='major-autocomplete', )
    )

    #crispy forms
    # helper = FormHelper()
    # #helper.add_input(Submit('Search', 'Search', css_class='btn btn-success", style='background: green !important'')   )
    # helper.layout = Layout(
    # Div(
    #     'major',
    #     style='background: green !important',
    #     css_id='test'
    #
    # ),
    #     Submit('Search', 'Search', css_class='btn btn-success", style='background: green !important'')
    # )
    # helper.form_show_labels = False

    class Meta:
        model = Collegemajor
        fields = ()


class MajorFormMasters(forms.ModelForm):
    major = forms.ModelChoiceField(
        # only searches for majors
        queryset=Collegemajor.objects.values_list('cipdesc'),
        widget=autocomplete.ModelSelect2(url='major-autocomplete-masters', )
    )

    class Meta:
        model = Collegemajor
        fields = ()




"""
Form that assist in autocomplete for school selection
"""


class SchoolForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        # only searches for majors
        queryset=Collegemajor.objects.values_list('instnm'),
        widget=autocomplete.ModelSelect2(url='school-autocomplete', )
    )

    class Meta:
        model = Collegemajor
        fields = ()


class SchoolFormMasters(forms.ModelForm):
    school = forms.ModelChoiceField(
        # only searches for majors
        queryset=Collegemajor.objects.values_list('instnm'),
        widget=autocomplete.ModelSelect2(url='school-autocomplete-masters', )
    )

    class Meta:
        model = Collegemajor
        fields = ()

