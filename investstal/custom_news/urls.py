# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import DateDetailView
from easy_news.models import News
from .views import news_root

urlpatterns = [
    url(r'^$', news_root, name='news_root'),
    url(r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(queryset=News.objects.filter(show=True), date_field='date', month_format='%m', slug_field='slug'),
        name='news_detail'
    )
]
