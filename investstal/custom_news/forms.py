# -*- coding: utf-8 -*-
from django import forms
from .models import NewsRoot


class NewsRootAdminForm(forms.ModelForm):
    class Meta:
        model = NewsRoot
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
        }
