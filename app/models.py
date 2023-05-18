from django.db import models

# Create your models here.


class House(models.Model):
    id = models.IntegerField(primary_key=True)
    Address = models.CharField(max_length=300)
    Zip = models.CharField(max_length=300)
    Price = models.IntegerField()
    Area = models.FloatField()
    Room = models.IntegerField()
    Lon = models.FloatField()
    Lat = models.FloatField()

class Data(models.Model):
    id = models.IntegerField(primary_key=True)
    Area = models.FloatField()
    Rooms = models.IntegerField()
    Lon = models.FloatField()
    Lat = models.FloatField()