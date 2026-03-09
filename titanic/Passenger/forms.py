from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Passenger

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = '__all__'
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
class SurvivalForm(forms.Form):
    survived = forms.BooleanField(
        required=False, 
        label='Survived',
        widget=forms.CheckboxInput()
    )