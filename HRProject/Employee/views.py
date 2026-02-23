from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from .models import Dept, Emp
from .forms import DeptForm, EmpForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

# def emp_list(request):
#     emps = Emp.objects.select_related('deptno').all()
#     depts = Dept.objects.all()
#     return render(request, 'Employee/index.html', {'emps': emps, 'depts': depts})

class DeptListView(ListView):
    model = Dept
    context_object_name = 'depts'

class DeptDetailView(DetailView):
    model = Dept

class DeptCreateView(CreateView):
    model = Dept
    form_class = DeptForm
    success_url = reverse_lazy('dept-list')

class DeptUpdateview(UpdateView):
    model = Dept
    form_class = DeptForm
    success_url = reverse_lazy('dept-list')

class DeptDeleteview(DeleteView):
    model = Dept
    success_url = reverse_lazy('dept-list')

# Employee CRUD

# 1. READ (List)
class EmpListView(ListView):
    model = Emp
    context_object_name = 'emps'

# 2. READ (Detail)
class EmpDetailView(DetailView):
    model = Emp

# 3. CREATE
class EmpCreateView(CreateView):
    model = Emp
    form_class = EmpForm
    success_url = reverse_lazy('emp-list')

# 4. UPDATE
class EmpUpdateView(UpdateView):
    model = Emp
    form_class = EmpForm
    success_url = reverse_lazy('emp-list')

# 5. DELETE
class EmpDeleteView(DeleteView):
    model = Emp
    success_url = reverse_lazy('emp-list')

