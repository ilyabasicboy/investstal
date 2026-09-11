# -*- coding: utf-8 -*-
from django import forms
from .models import Category, ParameterInline, ParameterValue, Product, Root, Section
from django.contrib.admin.widgets import FilteredSelectMultiple


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


class CategoryAdminForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
            'products': FilteredSelectMultiple(verbose_name='Товары', is_stacked=False),

        }


class ParameterInlineAdminForm(forms.ModelForm):

    class Meta:
        model = ParameterInline
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParameterInlineAdminForm, self).__init__(*args, **kwargs)

        parameter_group = self.initial.get('group')
        if parameter_group:
            values = [(None, '---------')] + [
                (parameter.id, parameter.value)
                for parameter in ParameterValue.objects.filter(parameter_group=parameter_group)
            ]
            self.fields['value'].choices = values
