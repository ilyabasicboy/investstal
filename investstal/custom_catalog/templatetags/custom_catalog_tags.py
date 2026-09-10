# -*- coding: utf-8 -*-
from django import template
from investstal.custom_attachment.utils import attach_images_list

from investstal.custom_catalog.models import CatalogItem


register = template.Library()


@register.simple_tag
def get_catalog_items(type=None, role=u'обложка', group=None):
      """
        Что делает:
            * Формирует список элементов каталога,
            * Для каждого ищет список AttchmentImage,
            * Задаёт каждому элементу список изображений в качестве атрибута "images"

            Решение N+1 проблемы
      """
      items = CatalogItem.objects.filter()

      if type is not None:
          items = items.filter(type=type)

      items = list(
          items
          # Добавить в подборку foreign key категории и разделы, сокращает количество запросов в бд
          .select_related('section', 'category')
          .order_by('order_key')
      )

      catalog_objects = [
          item.catalog_item
          for item in items
          if item.catalog_item
      ]

      attach_images_list(catalog_objects, role=role, group=group)

      return items


