from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class city(models.Model):
    cityName = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.cityName}"

class days(models.Model):
    day = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.day}"

class trains(models.Model):
    trainNo = models.IntegerField() 
    trainName = models.CharField(max_length=20, default="Express")
    origin = models.ForeignKey(city, on_delete = models.CASCADE, related_name="start")
    destination = models.ForeignKey(city,  on_delete = models.CASCADE, related_name="end")
    travelTime = models.IntegerField()
    startTime = models.CharField(max_length=4)
    endTime = models.CharField(max_length=4)
    travelDays = models.ManyToManyField(days)

    def __str__(self):
        return f"{self.trainName}({self.trainNo})"

    

class booking(models.Model):
    train = models.ForeignKey(trains, on_delete=models.CASCADE)
    date = models.CharField(max_length=15,default="Date")
    AC_I = models.IntegerField(default=48)
    AC_II = models.IntegerField(default=54)
    AC_III = models.IntegerField(default=288)
    Sleeper = models.IntegerField(default=576)


class passenger(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    age = models.IntegerField()
    Gender = models.CharField(max_length=6)
    PNR = models.CharField(max_length=11,default="XXX-XXXXXXX")
    seat = models.CharField(max_length=6, default="SL-B6")
    cost = models.IntegerField(default=3200)
    train_info = models.ManyToManyField(booking)
