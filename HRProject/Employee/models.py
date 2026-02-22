from django.db import models

class Dept (models.Model):
    deptno = models.IntegerField(primary_key=True)
    dname = models.CharField(max_length=50)
    loc = models.CharField(max_length=100)

    def __str__(self):
        return self.dname
    class Meta: 
        db_table='Dept'

class Emp(models.Model):
    empno = models.IntegerField(primary_key=True)
    ename = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    mgr = models.IntegerField(null=True,blank=True)
    hiredate = models.DateField()
    sal = models.DecimalField(max_digits=7, decimal_places=2)
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    deptno = models.ForeignKey(Dept, on_delete=models.CASCADE)

    def __str__(self):
        return self.ename
    class Meta:
        db_table = 'Emp'