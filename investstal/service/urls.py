# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings

from .views import handler404, handler500, sitemap, VendorCodeSearch


urlpatterns = [
    url(r'^sitemap.xml$', sitemap, name='sitemap'),
    url(r'^search/', VendorCodeSearch.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^404/$', handler404, name='handler404'),
        url(r'^500/$', handler500, name='handler500'),
    ] + urlpatterns
