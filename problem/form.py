from django import forms
from .models import *
from django.forms import widgets, Field


class ProblemFrom(forms.ModelForm):
    class Meta:
        model = Problem
        widgets = {
            'web_external_port': widgets.TextInput(attrs={'class': 'layui-input'}),
        }
        fields = [
            # 'web_external_port',
            # 'ssh_external_port',
            # 'template',
            # 'flag',
            # 'container_id',
            # 'status',
        ]
