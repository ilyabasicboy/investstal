# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from collections import OrderedDict
from attachment.models import AttachmentImage
from pages.models import Page
from investstal.custom_catalog.models import Product


register = template.Library()
try:
    PAGE_CT = ContentType.objects.get_for_model(Page)
    PRODUCT_CT = ContentType.objects.get_for_model(Product)
    LANG = settings.LANGUAGE_CODE
except:
    pass


@register.inclusion_tag('pages/parts/block_gallery.html', takes_context=True)
def show_block_gallery(context, key='all'):

    """ Отображает блок-галерею изображений с ролью 'галерея' разделенную по группам изображений
        принимает значение str:key = 'all'|'grouped_only'
        с ключем grouped_only - возвращает только группы изображений с заполенным полем группа
        с ключем all - возвращает так-же группу изображением с пустым полем группа"""

    obj = context.get("current_page")
    images = AttachmentImage.objects.filter(object_id=obj.id, content_type_id=PAGE_CT, role=settings.ROLE_GALLERY)
    # если не нужно выводить изображения без групп
    if key == "grouped_only":
        images = images.exclude(group="").exclude(group=None)
    images = images.order_by("group", "position")

    grouped_images = OrderedDict()
    if images.exists():
        groups = images.order_by("group").values_list("group", flat=True)
        empty_group_images = []
        for group in groups:
            if group:
                grouped_images[group] = []
        for image in images:
            if image.group:
                grouped_images[image.group].append(image)
            else:
                empty_group_images.append(image)

        if empty_group_images:
            grouped_images[None] = empty_group_images

    context["object_dict"] = grouped_images
    return context


@register.inclusion_tag('catalog/parts/block_cards.html', takes_context=True)
def show_block_products(context):

    """ Возвращает список товаров выбранных для страницы """

    obj = context.get('current_page')
    data = []
    for product in Product.objects.filter(produser=obj, show=True).order_by('tree'):
        data.append({
            'title': product.title,
            'get_absolute_url': product.get_absolute_url(),
            'description': product.description,
            'image': AttachmentImage.objects
                .filter(content_type=PRODUCT_CT, object_id=product.id).first()
        })
    context.update({'object_list': data})
    return context