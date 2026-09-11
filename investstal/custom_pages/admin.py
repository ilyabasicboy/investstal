# -*- coding: utf-8 -*-
from os.path import join
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from pages import settings
from pages.admin import PageAdmin
from pages.models import Page, PageAlias, Media
from .models import Advantage, WorkStep
from ..custom_attachment.models import CustomAttachmentImage
from ..custom_attachment.forms import CustomAttachmentImageForm


from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


@admin.register(Advantage)
class AdvantageAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Advantage
    list_display = ['text', 'type']


class WorkStepInline(SortableInlineAdminMixin, admin.TabularInline):
    model = WorkStep
    extra = 0
    fields = ['order_key', 'text']


class CustomAttachmentImageInline(admin.TabularInline):
    model = CustomAttachmentImage
    form = CustomAttachmentImageForm
    extra = 0


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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        page = Page.objects.get(pk=object_id)

        # Insert custom images with groups
        custom_image_inline_exist = False
        page_templates = ['pages/gallery.html', 'pages/finishing.html']
        for inline in self.inlines:
            if inline is CustomAttachmentImageInline:
                custom_image_inline_exist = True
                if not page.template in page_templates:
                    self.inlines.remove(inline)

        if not custom_image_inline_exist and page.template in page_templates:
            self.inlines.insert(0, CustomAttachmentImageInline)

        return super(PageAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


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
