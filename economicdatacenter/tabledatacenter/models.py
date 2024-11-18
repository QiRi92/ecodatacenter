from django.db import models

# Create your models here.
class DataCountryByEconomic(models.Model):
    country = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    web = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    date = models.DateField()
    data = models.FloatField()

    def __str__(self):
        return self.country