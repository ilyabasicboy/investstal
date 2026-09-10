# -*- coding: utf-8 -*-
from django.urls import path

from .views import FilterGroupedImages, FilterGroupedImagesGallery


urlpatterns = [
    path('filter_images/<str:page_id>/', FilterGroupedImages.as_view(), name='filter_images'),
    path('filter_images_gallery/<str:page_ids>/', FilterGroupedImagesGallery.as_view(), name='filter_images_gallery'),
]
