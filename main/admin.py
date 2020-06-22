from django.contrib import admin
from main.models import Collegemajor
from main.forms import MajorForm

# Register your models here.
"""
Admin Model for Majors (Doesn't Work)
(Should be implemented for both schools & majors
"""
# class MajorAdmin(admin.ModelAdmin):
#     form = MajorForm
#
# admin.site.register(Collegemajor, MajorForm)