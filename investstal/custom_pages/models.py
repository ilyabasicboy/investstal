from django.core.exceptions import ValidationError
from django.db import models
from attachment.settings import ATTACHMENT_UPLOAD_DIR
from pages.models import Page
from investstal.custom_catalog.models import Category, Section


ADVANTAGE_TYPES = (
    (0, 'Преимущество компании'),
    (1, 'Преимущество заказа'),
)


class Advantage(models.Model):

    class Meta:
        verbose_name = u'Преимущество'
        verbose_name_plural = u'Преимущества'
        ordering = ['order_key', ]

    order_key = models.PositiveIntegerField(
        verbose_name=u'',
        default=0,
        blank=False, null=False
    )
    text = models.TextField(
        verbose_name=u'Текст',
        null=True,
        blank=True
    )
    type = models.IntegerField(
        verbose_name=u'тип преимущества',
        default=0,
        choices=ADVANTAGE_TYPES
    )
    icon = models.FileField(
        verbose_name=u'Иконка',
        null=True,
        blank=True,
        upload_to=ATTACHMENT_UPLOAD_DIR
    )

    def __str__(self):
        return self.text or ''
