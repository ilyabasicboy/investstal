# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from easy_news.models import News
from pages.models import Page
from catalog.utils import get_content_objects, get_sorted_content_objects

from investstal.custom_news.models import NewsRoot
from investstal.custom_catalog. models import Root


register = template.Library()
try:
    NEWS_CT = ContentType.objects.get_for_model(News)
    PAGE_CT = ContentType.objects.get_for_model(Page)
    LANG = settings.LANGUAGE_CODE
except:
    pass


def get_page_children_data(page):

    """ Возвращает данные о потомках страницы """

    data = []
    for child in page.get_children().filter(status=Page.PUBLISHED):
        data.append({
            'title': child.title(),
            'get_absolute_url': child.get_absolute_url(),
            'children': get_page_children_data(child)
        })
    return data


def get_catalog_children(node):

    """ Возвращает данные о потомках элемента каталога """

    data = []
    for child in get_sorted_content_objects(get_content_objects(node.get_children())):
        if child.__class__.__name__ in settings.CATALOG_SITEMAP_HTML_MODELS:
            data.append({
                'title': child.title,
                'get_absolute_url': child.get_absolute_url(),
                'children': get_catalog_children(child.tree.get())
            })
    return data


@register.inclusion_tag('service/parts/block_sitemap.html', takes_context=True)
def show_block_sitemap(context):

    """ Отображение блока карты сайта """

    data = []
    for page in Page.objects.navigation().order_by("tree_id"):
        data.append({
            'title': page.title(),
            'get_absolute_url': page.get_absolute_url(),
            'children':  get_page_children_data(page)
        })

    catalog_root = Root.objects.all().first()
    if catalog_root:
        catalog_data = []
        for child in get_sorted_content_objects(get_content_objects(catalog_root.tree.get().get_children())):
            if child.__class__.__name__ in settings.CATALOG_SITEMAP_HTML_MODELS:
                catalog_data.append({
                    'title': child.title,
                    'get_absolute_url': child.get_absolute_url(),
                    'children': get_catalog_children(child.tree.get())
                })
        data.append({
            'title': catalog_root.title,
            'get_absolute_url': catalog_root.get_absolute_url(),
            'children': catalog_data
        })

    for page in Page.objects.navigation().order_by("tree_id"):
        data.append({
            'title': page.title(),
            'get_absolute_url': page.get_absolute_url(),
            'children': get_page_children_data(page)
        })
    context['object_list'] = data
    return context
