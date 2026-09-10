# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import CustomAttachmentImageForm, CustomImageGroupForm
from .models import CustomAttachmentImage, CustomImageGroup


@admin.register(CustomImageGroup)
class CustomImageGroupAdmin(admin.ModelAdmin):
    model = CustomImageGroup
    form = CustomImageGroupForm


@admin.register(CustomAttachmentImage)
class CustomAttachmentImageAdmin(admin.ModelAdmin):
    model = CustomAttachmentImage
    form = CustomAttachmentImageForm
    list_display = ['title', 'page', 'order_key']
    list_filter = ['page', 'image_group']
    search_fields = ['title']
