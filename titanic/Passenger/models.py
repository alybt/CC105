from django.db import models

class Passenger(models.Model):
    passenger   = models.IntegerField(primary_key=True)
    pclass      = models.IntergerField(max_length= 1)
    name        = models.CharField(max_length=225)
    sex         = models.CharField(max_length=10)
    age 	    = models.DecimalField(max_length=3, decimal_places = 3)
    sibsp       = models.IntegerField(max_length = 200)
    parch       = models.IntegerField(max_length = 1)	
    ticket	    = models.CharField(max_length=225)
    fare	    = models.DecimalField(max_length=3, decimal_places = 3)
    cabin	    = models.CharField(max_length=225)
    embarked	= models.CharField(max_length=225)
    boat	    = models.CharField(max_length=2)
    body	    = models.IntegerField(max_length=225)
    home.dest   = models.CharField(max_length=225)

    class Meta:
        model = Passenger
        fields = ['survived']

    def __str(self):
        return self.pname 

