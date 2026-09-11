# -*- coding: utf-8 -*-
from os.path import join
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from pages import settings
from pages.admin import PageAdmin
from pages.models import Page, PageAlias, Media
from .models import Advantage, WorkStep

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


@admin.register(Advantage)
class AdvantageAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Advantage
    list_display = ['text', 'type']


class WorkStepInline(SortableInlineAdminMixin, admin.TabularInline):
    model = WorkStep
    extra = 0
    fields = ['order_key', 'text']


class CustomPageAdmin(PageAdmin):
    inlines = list(PageAdmin.inlines) + [WorkStepInline]


    def get_inline_instances(self, request, obj=None):
        inline_instances = super(CustomPageAdmin, self).get_inline_instances(request, obj)
        if obj and obj.template == 'pages/frontpage.html':
            return inline_instances
        return [
            inline for inline in inline_instances
            if not isinstance(inline, WorkStepInline)
        ]

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
