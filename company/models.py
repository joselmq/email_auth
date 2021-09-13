from django.db import models
from company.fields import RutField
# from itertools import cycle
# import re


# class CompanyQueryset(models.QuerySet):
#
#     def annotate_sender_invoice_count(self):
#         # company.invoice_count
#         ...
#
#
# class CompanyManager(models.Manager):
#
#     def sme(self):
#         return self.filter(is_sme=True, is_active=True)


class Company(models.Model):
    rut = RutField(max_length=11)
    name = models.CharField(max_length=30)
    is_sme = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # objects = CompanyManager()


class Invoice(models.Model):
    total = models.IntegerField()
    sender = models.ForeignKey(Company,
                               on_delete=models.CASCADE,
                               related_name='sender_invoice',)
    receiver = models.ForeignKey(Company,
                                 on_delete=models.CASCADE,
                                 related_name='receiver_invoice',)

# get all invoices where the given company is the sender
# get all invoices where the given company is the receiver

# get all companies is_sme=True, is_active=True qs

# Company.objects.filter(name__startswith='a').filter(is_sme=True, is_active=True)
#
# Company.objects.sme()
#
#
# Company.objects.company_with_a().active_sme()
