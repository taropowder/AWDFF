from django import forms
from .models import *
from django.forms import widgets, Field


class ProblemFrom(forms.Form):
    flag = forms.CharField()
    token = forms.CharField()
