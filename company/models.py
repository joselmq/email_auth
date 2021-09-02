from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30)


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bill = models.IntegerField()
