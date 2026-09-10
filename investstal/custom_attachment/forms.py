# -*- coding: utf-8 -*-
from attachment.widgets import ImagePreviewWidget
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import CustomAttachmentImage, CustomImageGroup


class CustomImageGroupForm(forms.ModelForm):
    class Meta:
        model = CustomImageGroup
        fields = '__all__'
        widgets = {
            'title': forms.TextInput,
            'images': FilteredSelectMultiple(verbose_name=u'Группы изображений', is_stacked=False),
        }


class CustomAttachmentImageForm(forms.ModelForm):
    class Meta:
        model = CustomAttachmentImage
        fields = '__all__'
        widgets = {
            'title': forms.TextInput,
            'image': ImagePreviewWidget,
            'image_group': FilteredSelectMultiple(verbose_name=u'Группы изображений', is_stacked=False),
        }
