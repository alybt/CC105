from django.shortcuts import render
from .models import Emp, Dept

def emp_list(request):
    emps = Emp.objects.select_related('deptno').all()
    depts = Dept.objects.all()
    return render(request, 'Employee/index.html', {'emps': emps, 'depts': depts})

