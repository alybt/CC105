from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from .models import Passenger
from .forms import PassengerForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
 
# 1. READ (List)
class PassengerListView(ListView):
    model = Passenger
    context_object_name = 'passengers'

# 2. READ (Detail)
class PassengerDetailView(DetailView):
    model = Passenger

# 3. CREATE
class PassengerCreateView(CreateView):
    model = Passenger
    form_class = PassengerForm
    success_url = reverse_lazy('passenger-list')

# 4. UPDATE
class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerForm
    success_url = reverse_lazy('passenger-list')

# 5. DELETE
class PassengerDeleteView(DeleteView):
    model = Passenger
    success_url = reverse_lazy('passenger-list')

def passenger_view(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PassengerForm()
    return render(request, 'passenger.html', {'form': form})
