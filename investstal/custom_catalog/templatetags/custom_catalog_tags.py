# -*- coding: utf-8 -*-
from django import template
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects
from collections import defaultdict

from investstal.custom_catalog.models import CatalogItem


register = template.Library()


def attach_images(objects, role=None, group=None):
      objects = list(objects)

      if not objects:
          return objects

      objects_by_model = defaultdict(list)

      for obj in objects:
          if obj.pk:
              objects_by_model[obj.__class__].append(obj)

      if not objects_by_model:
          for obj in objects:
              obj.images = []
          return objects

      content_types = ContentType.objects.get_for_models(*objects_by_model.keys())

      images_by_object = defaultdict(list)

      for model, model_objects in objects_by_model.items():
          content_type = content_types[model]
          object_ids = [obj.pk for obj in model_objects]

          images = AttachmentImage.objects.filter(
              content_type=content_type,
              object_id__in=object_ids,
          ).order_by('position', 'id')

          if role is not None:
              images = images.filter(role=role)

          if group is not None:
              images = images.filter(group=group)

          for image in images:
              images_by_object[(content_type.id, image.object_id)].append(image)

      for obj in objects:
          content_type = content_types.get(obj.__class__)
          obj.images = images_by_object.get(
              (content_type.id, obj.pk),
              []
          ) if content_type and obj.pk else []

      return objects


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

      attach_images(catalog_objects, role=role, group=group)

      return items