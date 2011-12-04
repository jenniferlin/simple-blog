from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from profiles.models import *


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user')
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')