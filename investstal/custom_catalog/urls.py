# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from .views import FilterProductViewFp, change_parameters, facing_popup, parameter_popup

urlpatterns = [
    url('parameters_list/', change_parameters, name='change_parameters_list'),
    # url(r'^filter_products/$', FilterProductView.as_view(), name='filter_products'),
    url(r'^filter_products_fp/$', FilterProductViewFp.as_view(), name='filter_products_fp'),
    # url('parameters_list/', change_parameters, name='change_parameters_list'),
    url('^facing_popup/(?P<obj_id>.*)/$', facing_popup, name='facing_popup'),
    url('^parameter_popup/(?P<obj_id>.*)/$', parameter_popup, name='parameter_popup'),
    # path('filter_images_gallery_object/<str:object_id>/<str:ct_id>/', FilterImagesObject.as_view(), name='filter_images_gallery_object'),
]
