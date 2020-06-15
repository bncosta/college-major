from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Collegemajor(models.Model):
    instnm = models.TextField(blank=True, null=True)
    control = models.TextField(blank=True, null=True)
    main = models.TextField(blank=True, null=True)
    cipcode = models.TextField(blank=True, null=True)
    cipdesc = models.TextField(blank=True, null=True)
    credlev = models.TextField(blank=True, null=True)
    creddesc = models.TextField(blank=True, null=True)
    count = models.TextField(blank=True, null=True)
    debtmedian = models.TextField(blank=True, null=True)
    debtpayment10yr = models.TextField(blank=True, null=True)
    debtmean = models.TextField(blank=True, null=True)
    titleivcount = models.TextField(blank=True, null=True)
    earningscount = models.TextField(blank=True, null=True)
    md_earn_wne = models.TextField(blank=True, null=True)
    ipedscount1 = models.TextField(blank=True, null=True)
    ipedscount2 = models.TextField(blank=True, null=True)
    id = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'collegemajor'

