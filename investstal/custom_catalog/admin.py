# -*- coding:utf-8 -*-
from django.contrib import admin
from catalog.admin import CatalogItemBaseAdmin
from .models import Category, CatalogItem, Product, Root, Section
from .forms import CategoryAdminForm, ProductAdminForm, RootAdminForm, SectionAdminForm

from adminsortable2.admin import SortableAdminMixin


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
    fields = ['title', 'slug', 'show', 'price', 'description', 'main_content']


@admin.register(Section)
class SectionAdmin(CatalogItemBaseAdmin):

    model = Section
    form = SectionAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    fields = ['title', 'slug', 'show', 'long_title']


@admin.register(Category)
class CategoryAdmin(CatalogItemBaseAdmin):

    model = Category
    form = CategoryAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    fields = ['title', 'slug', 'show', 'long_title']


@admin.register(CatalogItem)
class CatalogItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    extra = 0
    list_display = ['type', 'section', 'category']
