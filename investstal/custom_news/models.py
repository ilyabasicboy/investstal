# -*- coding: utf-8 -*-
from django.db import models
from easy_news.models import News
from tinymce.models import HTMLField
from django.utils import timezone
from django.urls import reverse


class NewsRoot(models.Model):
    class Meta:
        verbose_name = u'Страница списка новостей'
        verbose_name_plural = verbose_name

    title = models.CharField(verbose_name=u'заголовок', max_length=300)
    last_modified = models.DateTimeField(auto_now=True)
    main_content = HTMLField(verbose_name=u'контент', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент внизу страницы', default='', blank=True)

    @property
    def news(self):

        """ Возвращает список новостей """

        return News.objects.filter(show=True, date__lte=timezone.now())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_root')
