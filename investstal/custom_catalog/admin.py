# -*- coding:utf-8 -*-
from django.contrib import admin
from django.forms import widgets
from catalog.admin import CatalogItemBaseAdmin
from .models import Category, CatalogItem, ParameterGroup, ParameterInline, ParameterValue, Product, Root, Section, Thermal
from .forms import CategoryAdminForm, ParameterInlineAdminForm, ProductAdminForm, RootAdminForm, SectionAdminForm, ThermalForm

from adminsortable2.admin import SortableAdminMixin


class ParameterInlineAdmin(admin.TabularInline):
    model = ParameterInline
    form = ParameterInlineAdminForm
    fields = ['group', 'value']
    extra = 0

    @property
    def media(self):
        return super().media + widgets.Media(js=('js/admin/parameterinline.js',))


class CustomCatalogItemBaseAdmin(CatalogItemBaseAdmin):

    def view_on_site(self, obj):
        return obj.get_absolute_url()


@admin.register(Root)
class RootAdmin(CatalogItemBaseAdmin):

    def has_add_permission(self, request):
        return not bool(Root.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    model = Root
    form = RootAdminForm
    fields = ['title', 'long_title']


@admin.register(Product)
class ProductAdmin(CatalogItemBaseAdmin):

    model = Product
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    inlines = [ParameterInlineAdmin, ]


@admin.register(Section)
class SectionAdmin(CatalogItemBaseAdmin):

    model = Section
    form = SectionAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    inlines = [ParameterInlineAdmin, ]


@admin.register(Category)
class CategoryAdmin(CustomCatalogItemBaseAdmin):

    model = Category
    form = CategoryAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    list_display = ['title', ]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        try:
            priority_fields = ['show', 'slug', 'title', 'long_title', 'group', ]
            remaining_fields = [f for f in fields if f not in priority_fields]
            ordered_fields = []

            for field in priority_fields:
                if field in fields:
                    ordered_fields.append(field)

            ordered_fields.extend(remaining_fields)

            return ordered_fields
        except:
            return fields


@admin.register(CatalogItem)
class CatalogItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    extra = 0
    list_display = ['type', 'section', 'category']


@admin.register(ParameterValue)
class ParameterValueAdmin(admin.ModelAdmin):
    model = ParameterValue
    list_filter = ['parameter_group']
    list_display = ['__str__', 'show_in_additional_choices', 'extra_price', 'show_images']
    list_editable = ['show_in_additional_choices', 'extra_price', 'show_images']


@admin.register(ParameterGroup)
class ParameterGroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = ParameterGroup
    ordering = ['order_key']
    list_display = ['title', 'slug', 'group_type', ]
    list_editable = ['group_type', ]
    list_filter = ['group_type']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Thermal)
class ThermalAdmin(admin.ModelAdmin):
    model = Thermal
    form = ThermalForm
    inlines = [ParameterInlineAdmin, ]

    @property
    def media(self):
        shared = (
                super().media + widgets.Media(
            js=('admin/js/vendor/jquery/jquery.min.js',)))

        return shared
