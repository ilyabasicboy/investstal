# -*- coding: utf-8 -*-
from django import forms
from .models import ErrorPage, SiteSettings


class ErrorPageAdminForm(forms.ModelForm):

    class Meta:
        model = ErrorPage
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'type': forms.Select(attrs={'class': 'large-input'}),
        }

    def clean(self):
        type = self.cleaned_data.get('type')
        if ErrorPage.objects.filter(type=type).exclude(id=self.instance.id).exists():
            self.add_error('type', u'Страница ошибки с таким типом уже существует!')
        return self.cleaned_data


class SiteSettingsAdminForm(forms.ModelForm):

    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'domain': forms.TextInput(attrs={'class': 'large-input'}),
            'name': forms.TextInput(attrs={'class': 'large-input'}),
            'robots': forms.Textarea(attrs={'class': 'large-input'})
        }
