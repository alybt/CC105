from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from .models import Emp, Dept
from .forms import DeptForm, EmpForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

def emp_list(request):
    emps = Emp.objects.select_related('deptno').all()
    depts = Dept.objects.all()
    return render(request, 'Employee/index.html', {'emps': emps, 'depts': depts})

#Dept CRUD
class DeptListView(ListView):
    model = Dept
    context_object_name = 'depts'

class DeptDetailView(DetailView):
    model = Dept

class DeptCreateView(CreateView):
    model = Dept
    form_class = DeptForm
    success_url = reverse_lazy('dept-list')

class DeptUpdateView(UpdateView):
    model = Dept
    form_class = DeptForm
    success_url = reverse_lazy ('dept-list')

class DeptDeleteView (DeleteView):
    model = Dept
    success_url = reverse_lazy ('dept-list')

#Emp CRUD
class EmpListView(ListView):
    model = Emp
    context_object_name = 'emps'

class EmpDetailView(DetailView):
    model = Emp

class EmpCreateView(CreateView):
    model = Emp
    form_class = EmpForm
    success_url = reverse_lazy('emp-list')

class EmpUpdateView(UpdateView):
    model = Emp
    form_class = EmpForm
    success_url = reverse_lazy ('emp-list')

class EmpDeleteView (DeleteView):
    model = Emp
    success_url = reverse_lazy ('emp-list')