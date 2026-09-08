# -*- coding: utf-8 -*-
from django import forms
from .models import Section, Product, Root


class RootAdminForm(forms.ModelForm):

    class Meta:
        model = Root
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'long_title': forms.TextInput(attrs={'class': 'large-input'}),
        }


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
            'price': forms.TextInput(attrs={'class': 'large-input'}),
        }


class SectionAdminForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
        }


