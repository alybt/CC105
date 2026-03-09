from django.db import models 

class Passenger(models.Model): 
    survived = models.IntegerField() 
    pclass = models.IntegerField()
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10)
    age = models.FloatField(null=True, blank=True)
    sibsp = models.IntegerField()
    parch = models.IntegerField()
    ticket = models.CharField(max_length=100)
    fare = models.FloatField(null=True, blank=True)
    cabin = models.CharField(max_length=100, null=True, blank=True)
    embarked = models.CharField(max_length=100, null=True, blank=True)
    boat = models.CharField(max_length=100, null=True, blank=True)
    body = models.IntegerField(null=True, blank=True)
    home_dest = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

