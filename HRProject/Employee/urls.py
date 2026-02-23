from django.urls import path
from . import views

urlpatterns = [
    #Dept 
    path('dept/', views.DeptListView.as_view(), name='dept-list'),
    path('dept/<int:pk>/', views.DeptDetailView.as_view(), name = 'dept-detail'),
    path('dept/new', views.DeptCreateView.as_view(), name = 'dept-create'),
    path('dept/<int:pk>/update', views.DeptDetailView.as_view(), name = 'dept-update'),
    path('dept/<int:pk>/delete', views.DeptDetailView.as_view(), name = 'dept-delete'),

    #Emp
    path('', views.emp_list, name = 'emp-list'),
    path('emp/', views.EmpListView.as_view(), name= 'emp-list'),
    path('emp/<int:pk>/', views.EmpDetailView.as_view(), name= 'emp-detail'),
    path('emp/new', views.EmpCreateView.as_view(), name='emp-create'),
    path('emp/<int:pk>/update', views.EmpUpdateView.as_view(), name= 'emp-update'),
    path('emp/<int:pk>/delete', views.EmpDeleteView.as_view(), name= 'emp-delete'),
]