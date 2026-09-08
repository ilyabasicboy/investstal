# -*- coding utf-8 -*-
from django.contrib import admin
from django.contrib.sites.admin import Site
from .models import ErrorPage, SiteSettings
from .forms import ErrorPageAdminForm, SiteSettingsAdminForm


@admin.register(ErrorPage)
class ErrorPageAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.generate_static_page(request)

    model = ErrorPage
    form = ErrorPageAdminForm
    list_display = ('type', 'title')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    model = SiteSettings
    form = SiteSettingsAdminForm

    def save_model(self, request, obj, form, change):
        obj.generate_robots_file()
        obj.save()

try:
    admin.site.unregister(Site)
except:
    pass