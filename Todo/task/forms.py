from django import forms
from .models import  *
from django.contrib.auth.models import User



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title' , 'desc']