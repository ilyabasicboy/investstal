# -*- coding: utf-8 -*-
from os.path import join
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from pages import settings
from pages.admin import PageAdmin
from pages.models import Page, PageAlias, Media


class CustomPageAdmin(PageAdmin):

    class Media:

        """ Добавлены кастомные js и сss """

        css = {
            'all': [
                join(settings.PAGES_STATIC_URL, 'css/rte.css'),
                join(settings.PAGES_STATIC_URL, 'css/pages.css'),
                'css/admin/custom_pages.css',  # Доработка change form стилей
                'css/admin/common.css'  # Добавление глобальных стилей
            ]
        }
        js = [
            join(settings.PAGES_STATIC_URL, 'javascript/jquery.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/jquery.rte.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/pages.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/pages_list.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/pages_form.js'),
            'js/admin/pages_form_extra.js',
            join(settings.PAGES_STATIC_URL, 'javascript/jquery.query-2.1.7.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/iframeResizer.min.js'),
        ]


try:
    admin.site.unregister(Media)
    admin.site.unregister(PageAlias)
except NotRegistered:
    pass

try:
    admin.site.unregister(Page)
    admin.site.register(Page, CustomPageAdmin)
except NotRegistered:
    pass
