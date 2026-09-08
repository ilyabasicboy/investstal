# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.shortcuts import render
from easy_news.models import News
from pages.models import Page
from investstal.custom_news.models import NewsRoot
from .models import ErrorPage


def handler404(request, exception=None):
    obj, _ = ErrorPage.objects.get_or_create(type='404')
    obj.generate_static_page(request)
    return render(request, 'service/404.html', {'object': obj}, status=404)


def handler500(request):
    obj, _ = ErrorPage.objects.get_or_create(type='500')
    obj.generate_static_page(request)
    return render(request, 'service/500.html', {'object': obj}, status=500)


def sitemap(request):
    sitemaps = {
        'pages': GenericSitemap({
            'queryset': Page.objects.filter(status=Page.PUBLISHED),
            'date_field': 'last_modification_date',
        }),
        'news': GenericSitemap({
            'queryset': News.objects.filter(show=True),
            'date_field': 'date',
        }),
        'news_root': GenericSitemap({
            'queryset': NewsRoot.objects.all(),
            'date_field': 'last_modified',
        }),
    }
    return sitemap_view(request, sitemaps, template_name='service/sitemap.xml')
