from django.forms import forms, ModelForm
from .models import *

# dappx/forms.py
from django import forms
from django.db import models
from .models import UserProfileInfo
from django.contrib.auth.models import User
# from models import ModelForm
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
# from django.forms import SharingForms
# from .models import Images
from taggit.managers import TaggableManager

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('FullName', 'portfolio_site', 'profile_pic', 'BirthDate', 'mobile', 'Country')




class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'target', 'start_date', 'end_date', 'user', 'category', 'tags', 'main_pic']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']


class CommentReport(forms.ModelForm):
    class Meta:
        model = commentReport
        fields = ['subject', 'details']


class ReportProject(forms.ModelForm):
    class Meta:
        model = projectReport
        fields = ['subject', 'details']