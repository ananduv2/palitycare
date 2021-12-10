from .models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.db.models import Q

class AddServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['category']