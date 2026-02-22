from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Dept, Employee

class DeptFrom (form.ModelForm):
    class Meta: 
        model = Dept
        fields = '__all__ '
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))

class EmpForm(forms.ModelForm):
    class Meta: 
        model = Emp
        fields = '__all__' 
        widgets = {
            'hiredate': forms.DateInput (attrs= {'type': 'date'}),
        }
    helper = FormerHelper()
    helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))

