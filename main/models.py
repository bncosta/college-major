from django.db import models


# class Collegemajor(models.Model):
#     instnm = models.TextField(blank=True, null=True)
#     control = models.TextField(blank=True, null=True)
#     main = models.TextField(blank=True, null=True)
#     cipcode = models.TextField(blank=True, null=True)
#     cipdesc = models.TextField(blank=True, null=True)
#     credlev = models.TextField(blank=True, null=True)
#     creddesc = models.TextField(blank=True, null=True)
#     count = models.TextField(blank=True, null=True)
#     debtmedian = models.TextField(blank=True, null=True)
#     debtpayment10yr = models.TextField(blank=True, null=True)
#     debtmean = models.TextField(blank=True, null=True)
#     titleivcount = models.TextField(blank=True, null=True)
#     earningscount = models.TextField(blank=True, null=True)
#     md_earn_wne = models.TextField(blank=True, null=True)
#     ipedscount1 = models.TextField(blank=True, null=True)
#     ipedscount2 = models.TextField(blank=True, null=True)
#     id = models.TextField(primary_key=True)
#
#     class Meta:
#         managed = False
#         db_table = 'collegemajor'


class Collegemajor(models.Model):
    unitid = models.TextField(max_length=200, blank=True, null=True)
    opeid6 = models.TextField(max_length=200, blank=True, null=True)
    instnm = models.TextField(max_length=200, blank=True, null=True)
    control = models.TextField(max_length=200, blank=True, null=True)
    main = models.TextField(max_length=200, blank=True, null=True)
    cipcode = models.TextField(max_length=200, blank=True, null=True)
    cipdesc = models.TextField(max_length=200, blank=True, null=True)
    credlev = models.TextField(max_length=200, blank=True, null=True)
    creddesc = models.TextField(max_length=200, blank=True, null=True)
    count = models.TextField(max_length=200, blank=True, null=True)
    debtmedian = models.TextField(max_length=200, blank=True, null=True)
    debtpayment10yr = models.TextField(max_length=200, blank=True, null=True)
    debtmean = models.TextField(max_length=200, blank=True, null=True)
    titleivcount = models.TextField(max_length=200, blank=True, null=True)
    earningscount = models.TextField(max_length=200, blank=True, null=True)
    md_earn_wne = models.TextField(max_length=200, blank=True, null=True)
    ipedscount1 = models.TextField(max_length=200, blank=True, null=True)
    ipedscount2 = models.TextField(max_length=200, blank=True, null=True)
    id = models.TextField(max_length=200, primary_key=True)

    class Meta:
        managed = False
        db_table = 'collegemajor'