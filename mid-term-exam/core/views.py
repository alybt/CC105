from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Passenger
from .forms import PassengerForm

class PassengerListView(ListView):
    model = Passenger
    template_name = 'passenger_list.html'
    context_object_name = 'passengers'
    
    def get_paginate_by(self, queryset): 
        show_all = self.request.GET.get('show') == 'all'
        if show_all:
            return None  
        return 20

class PassengerDetailView(DetailView):
    model = Passenger
    template_name = 'passenger_detail.html'

class PassengerCreateView(CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'passenger_form.html' 
    success_url = reverse_lazy('passenger-list') 

class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'passenger_form.html' 
    success_url = reverse_lazy('passenger-list')

class PassengerDeleteView(DeleteView):
    model = Passenger
    template_name = 'passenger_confirm_delete.html'
    success_url = reverse_lazy('passenger-list')