# -*- coding: utf-8 -*-
from django import template
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects


register = template.Library()
