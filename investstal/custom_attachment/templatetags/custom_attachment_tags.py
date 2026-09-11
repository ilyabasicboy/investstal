# -*- coding: utf-8 -*-
from ast import literal_eval
import random

from attachment.models import AttachmentImage
from django import template
from django.contrib.contenttypes.models import ContentType
from pages.models import Page

from ..models import CustomAttachmentImage, CustomImageGroup

register = template.Library()


@register.filter
def role(images, role):
    """Get images with role"""
    try:
        return [image for image in images if image.role == role]
    except KeyError:
        return None


@register.filter
def exclude_role(images, role):
    """Get images without role"""
    try:
        return [image for image in images if image.role!=role]
    except KeyError:
        return None


@register.filter
def roles_several(images, roles):
    """Get images with role"""
    try:
        roles = roles.replace(' ', '').split(',')
        images_new = []
        for role in roles:
            if role == 'None':
                role = None
            images_new += [image for image in images if image.role == role]
        return images_new
    except KeyError:
        return None


@register.simple_tag
def get_images_for_groups(image_groups):
    images_id_list = image_groups.values_list('images', flat=True)
    return CustomAttachmentImage.objects.filter(id__in=images_id_list)


@register.filter
def shuffle(images):
    tmp = list(images)[:]
    random.shuffle(tmp)
    return tmp


@register.simple_tag
def get_images_for_groups_list(ids):
    try:
        if isinstance(ids, str):
            ids = literal_eval(ids)
        images_id_list = CustomImageGroup.objects.filter(id__in=ids).values_list('images', flat=True).distinct()
        return CustomAttachmentImage.objects.filter(id__in=images_id_list)
    except Exception:
        return CustomAttachmentImage.objects.none()


@register.simple_tag
def get_custom_images_groups(images):
    try:
        groups_ids = images.values_list('image_group', flat=True).distinct()
        res = CustomImageGroup.objects.filter(id__in=groups_ids)
    except Exception:
        res = CustomImageGroup.objects.none()

    return res


@register.simple_tag()
def get_images_for_page(page):
    if not page:
        return None

    result = CustomAttachmentImage.objects.filter(page=page)

    if not result or not result.exists():
        ct = ContentType.objects.get_for_model(Page)
        result = AttachmentImage.objects.filter(object_id=page.id, content_type=ct)

    return result
