from django.urls import path
from . import views

urlpatterns = [path('', views.emp_list, name='emp_list')]