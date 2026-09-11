# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import CustomAttachmentImageForm, CustomImageGroupForm
from .models import CustomAttachmentImage, CustomImageGroup


@admin.register(CustomImageGroup)
class CustomImageGroupAdmin(admin.ModelAdmin):
    model = CustomImageGroup
    form = CustomImageGroupForm