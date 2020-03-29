from django.db import models
from django.contrib.postgres.fields import ArrayField
class Labels(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
class Tags(models.Model):
    data = ArrayField(models.FloatField())
    label = models.IntegerField()
    used = models.BooleanField(default=False)
class Zeros(models.Model):
    true_label = models.IntegerField()
    data = ArrayField(models.FloatField())
    used = models.BooleanField(default=False)
class ToParse(models.Model):
    site = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    ptag = models.CharField(max_length=255)
    pptag = models.CharField(max_length=255)
    Cclass = models.CharField(max_length=255)
    pclass = models.CharField(max_length=255)
    ppclass = models.CharField(max_length=255)
class BoostModels(models.Model):
    Bmodel = models.BinaryField()
    label = models.IntegerField()