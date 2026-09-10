# -*- coding: utf-8 -*-
import os

from attachment.fields import ImagePreviewField
from attachment.settings import ATTACHMENT_CACHE_DIR, ATTACHMENT_IKSPECS, ATTACHMENT_UPLOAD_DIR
from django.db import models
from imagekit.models import ImageModel
from pages.models import Page


class CustomImageGroup(models.Model):
    class Meta:
        verbose_name = u'Группа изображений'
        verbose_name_plural = u'Группы изображений'

    title = models.TextField(
        verbose_name=u'Название группы',
        null=True
    )
    images = models.ManyToManyField(
        'CustomAttachmentImage',
        verbose_name=u'Изображения группы',
        blank=True,
    )

    def get_page_titles(self):
        try:
            pages_id = self.images.values_list('page', flat=True).distinct()
            pages = Page.objects.filter(id__in=pages_id)
            page_titles = [page.title() for page in pages if hasattr(page, 'title')]

            if page_titles:
                return u"({})".format(u', '.join(page_titles))
        except Exception:
            return ''

    def __str__(self):
        try:
            page_titles = self.get_page_titles()
            if page_titles:
                return u"{} {}".format(self.title, page_titles)
        except Exception:
            pass
        return self.title or u''

    @property
    def get_page_link(self):
        try:
            return self.images.first().page.get_absolute_url() if self.images.exists() else None
        except Exception:
            return None


class CustomAttachmentImage(ImageModel):
    """Изображения с группами"""

    class Meta:
        verbose_name = u'Изображение с группами'
        verbose_name_plural = u'Изображения с группами'
        ordering = ('order_key',)

    class IKOptions:
        spec_module = ATTACHMENT_IKSPECS
        cache_dir = ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    order_key = models.IntegerField(
        default=0,
        blank=False,
        null=False
    )
    image = ImagePreviewField(
        verbose_name=u'Изображение',
        upload_to=ATTACHMENT_UPLOAD_DIR,
        null=True,
        blank=True
    )
    title = models.TextField(
        verbose_name=u'Заголовок',
        null=True,
        blank=True
    )
    image_group = models.ManyToManyField(
        CustomImageGroup,
        through=CustomImageGroup.images.through,
        verbose_name=u'Группа изображений',
        blank=True,
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.image:
            return os.path.basename(self.image.url)
        return u''
