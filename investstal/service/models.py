# -*- coding: utf-8 -*-
import os
from types import MethodType
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from tinymce.models import HTMLField
from django.contrib.sites.models import Site
from django.shortcuts import reverse


class ErrorPage(models.Model):

    TYPE_404 = '404'
    TYPE_500 = '500'
    TYPES = (
        (TYPE_404, TYPE_404),
        (TYPE_500, TYPE_500)
    )

    class Meta:
        verbose_name = u'страница ошибки'
        verbose_name_plural = u'страницы ошибок'

    type = models.CharField(verbose_name=u'тип', max_length=255, choices=TYPES)
    title = models.CharField(verbose_name=u'заголовок', max_length=255, blank=True, null=True)
    main_content = HTMLField(verbose_name=u'контент', blank=True, null=True)

    def generate_static_page(self, request):
        context = {'object': self}
        rendered = render_to_string('service/base_%s.html' % self.type, context, request)
        file_dir = os.path.join(settings.PROJECT_ROOT, 'templates', 'service', '%s.html' % self.type)
        file = open(file_dir, 'wb')
        file.write(rendered.encode('utf-8'))
        file.close()
        return True

    def __str__(self):
        return self.type


if settings.DEBUG:

    def get_absolute_url(self):
        return reverse('handler%s' % self.type)

    ErrorPage.get_absolute_url = MethodType(get_absolute_url, ErrorPage)


class SiteSettings(Site):

    class Meta:
        verbose_name = u'настройки домена'
        verbose_name_plural = verbose_name

    robots = models.TextField(
        verbose_name=u'содержимое файла robots.txt', blank=True, null=True,
        default=u'user-agent: *\ndisallow: /'
    )

    fp_logo = models.FileField(
        verbose_name=u'Логотип для главной страницы', upload_to='upload',
        blank=True, null=True,
        help_text=u'Изображение 204 x 204 px (jpeg, jpg, png, svg).<br> '
                  u'Если не заполнено - отображается логотип по умолчанию'
    )

    def generate_robots_file(self   ):
        file_dir = os.path.join(settings.PROJECT_ROOT, 'templates', 'service', 'robots.txt')
        file = open(file_dir, 'wb')
        file.write(self.robots.encode('utf-8'))
        file.close()
        return True
