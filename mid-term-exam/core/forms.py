from django import forms
from .models import Passenger

class PassengerForm(forms.ModelForm): 
    SURVIVED_CHOICES = [(1, 'Yes'), (0, 'No')]
    SEX_CHOICES = [('male', 'Male'), ('female', 'Female')]
    CLASS_CHOICES = [(1, '1st Class'), (2, '2nd Class'), (3, '3rd Class')]
    EMBARKED_CHOICES = [('S', 'Southampton'), ('C', 'Cherbourg'), ('Q', 'Queenstown')] 
    survived = forms.ChoiceField(choices=SURVIVED_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    pclass = forms.ChoiceField(choices=CLASS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    embarked = forms.ChoiceField(choices=EMBARKED_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Passenger
        fields = '__all__'