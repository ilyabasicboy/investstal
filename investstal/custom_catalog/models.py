# -*- encoding: utf-8 -*-
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from tinymce.models import HTMLField
from catalog.models import CatalogBase
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects


class Root(CatalogBase):
    class Meta:
        verbose_name = u'корневая страница'
        verbose_name_plural = verbose_name

    slug = ''
    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(verbose_name=u'длинное название', max_length=400, blank=True, null=True)
    main_content = HTMLField(verbose_name=u'контент в начале страницы', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент в конце страницы', blank=True, null=True)

    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self, *args, **kwargs):
        return u'Корневая страница'

    def get_absolute_url(self):
        return reverse('catalog-root')

    @property
    def root_sections(self):

        """ Возвращает список разделов верхнего уровня"""

        return get_sorted_content_objects(
            get_content_objects(self.tree.get().get_children(), allowed_models=(Section,))
        )


class Product(CatalogBase):
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'

    leaf = True
    title = models.CharField(verbose_name=u'название', max_length=400)
    price = models.CharField(verbose_name=u'цена', max_length=255, blank=True, default='')
    description = models.TextField(verbose_name=u'короткое описание', default='', blank=True)
    main_content = HTMLField(verbose_name=u'основной контент', blank=True, null=True)

    @property
    def images(self):
        return AttachmentImage.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(Product),
            role=settings.ROLE_GALLERY
        )

    def __str__(self):
        return self.title


class Section(CatalogBase):
    class Meta:
        verbose_name = u'раздел'
        verbose_name_plural = u'разделы'

    title = models.CharField(verbose_name=u'название', max_length=400)
    description = models.TextField(verbose_name=u'короткое описание', blank=True, null=True)
    main_content = HTMLField(verbose_name=u'основной контент', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент в конце страницы', blank=True, null=True)

    def __str__(self):
        return self.title
