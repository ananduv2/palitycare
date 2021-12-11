from .models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

class AddServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['category']

class PublicUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','password1','password2']

class UserSignUpForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'mob','sex','house','street1','street2','city','district','state','pin']