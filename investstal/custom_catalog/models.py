# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Max, Min, Q, Avg
from django.shortcuts import reverse
from django.conf import settings
from django.core.cache import cache
from tinymce.models import HTMLField
from catalog.models import CatalogBase
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects
from django.core.exceptions import ValidationError
from itertools import chain
from investstal.custom_attachment.utils import attach_images_queryset


GROUP_CHOICES = (
    (1, 'По ценовому сегменту'),
    (2, 'По назначению'),
    (3, 'По особенностям'),
    (4, 'По отделке')
)


class CatalogMixin:

    def get_products(self):
        raise NotImplemented

    def get_products_count(self):
        result = cache.get(self.cache_key()+'_products_count', None)
        if not result:
            result = self.get_products().count()
            cache.set(self.cache_key()+'_products_count', result, 600000)
        return result

    def cache_key(self):
        return '%s_%d' % (self.__class__.__name__, self.id)

    def get_min_price(self):
        result = cache.get(self.cache_key()+'_min_price', 0)
        if not result:
            prices = self.get_products().aggregate(Min('price'))
            result = prices['price__min']
            cache.set(self.cache_key()+'_min_price', result, 600000)
        return result

    def get_max_price(self):
        result = cache.get(self.cache_key()+'_max_price', 0)
        if not result:
            prices = self.get_products().aggregate(Max('price'))
            result = prices['price__max']
            cache.set(self.cache_key()+'_max_price', result, 600000)
        return result

    def get_sorted_products(self):
        result = self.get_products()

        if hasattr(self, 'sort'):
            if self.sort == 'asc':
                result = result.order_by('price')
            elif self.sort == 'desc':
                result = result.order_by('-price')
            elif self.sort == 'popular':
                result = get_sorted_content_objects(result)
            else:
                result = result.order_by('-id')

        return result


class Root(CatalogBase, CatalogMixin):
    class Meta:
        verbose_name = u'корневая страница'
        verbose_name_plural = verbose_name

    slug = ''
    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(verbose_name=u'длинное название', max_length=400, blank=True, null=True)

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

    def get_products(self):
        result = cache.get(self.cache_key() + '_products')
        if result is None:
            result = Product.objects.filter(show=True).order_by('-id')
            cache.set(self.cache_key() + '_products', result, 600000)
        return result

    def get_catalog_data(self):
        result = cache.get(self.cache_key() + '_catalog_data')
        if result is None:
            result = {}
            for group_type, group_name in GROUP_CHOICES:
                group = get_sorted_content_objects(
                    list(
                        chain(
                            Category.objects.filter(group=group_type, show=True),
                            Section.objects.filter(group=group_type, show=True)
                        )
                    )
                )

                if group:
                    result[group_name] = group
            cache.set(self.cache_key() + '_catalog_data', result, 600000)
        return result

    def get_products_new(self):
        # result = cache.get(self.cache_key() + '_products_new')
        # if result is None:
        result = self.get_products().order_by('-created')[:150]
        # Подгрузить изображения
        result = attach_images_queryset(result)
            # cache.set(self.cache_key() + '_products_new', result, 600000)
        return result

    def get_products_new_categories(self):
        # result = cache.get(self.cache_key() + '_products_new_categories')
        # if result is None:
        products = self.get_products_new()
        result = Category.objects.filter(products__in=products).distinct()
            # cache.set(self.cache_key() + '_products_new_categories', result, 600000)
        return result


class Product(CatalogBase):
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'

    leaf = True
    title = models.CharField(verbose_name=u'название', max_length=400)
    price = models.CharField(verbose_name=u'цена', max_length=255, blank=True, default='')
    square_price = models.BooleanField(
        verbose_name=u'Цена за 1 кв.м',
        default=False,
    )
    description = models.TextField(verbose_name=u'короткое описание', default='', blank=True)
    main_content = HTMLField(verbose_name=u'основной контент', blank=True, null=True)
    created = models.DateTimeField(
        verbose_name="создан",
        auto_now_add=True,
        editable=False
    )

    def get_product_images(self):
        result = cache.get(self.cache_key() + '_product_images')
        if result is None:
            ct = ContentType.objects.get_for_model(Product)
            result = AttachmentImage.objects.filter(content_type=ct.id, object_id=self.id)
            cache.set(self.cache_key() + '_product_images', result, 600000)
        return result

    def get_vendor_code(self):
        return f'Арт.{self.id:05d}'

    def __str__(self):
        return self.title


class Section(CatalogBase, CatalogMixin):
    class Meta:
        verbose_name = u'раздел'
        verbose_name_plural = u'разделы'

    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400,
        null=True,
        blank=True
    )

    def get_products(self):
        result = cache.get(self.cache_key() + '_products')
        if result is None:
            result = Product.objects.filter(tree__parent__object_id=self.id, show=True)
            cache.set(self.cache_key() + '_products', result, 600000)
        return result

    def __str__(self):
        return self.title


class Category(CatalogBase, CatalogMixin):
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'

    title = models.CharField(verbose_name=u'название', max_length=400)
    products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name='товары'
    )
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400,
        null=True,
        blank=True
    )

    def get_products(self):
        result = cache.get(self.cache_key() + '_products')
        if result is None:
            result = self.products.filter(show=True)
            cache.set(self.cache_key() + '_products', result, 600000)
        return result

    def __str__(self):
        return self.title


CATALOG_ITEM_TYPES = (
    (0, 'блок "металлические двери" на главной'),
    (1, 'блок "также производим" на главной'),
)


class CatalogItem(models.Model):
    class Meta:
        verbose_name = u'Элемент каталога на страницах'
        verbose_name_plural = u'Элементы каталога на страницах'
        ordering = ['order_key', ]

    section = models.ForeignKey(
        Section,
        verbose_name=u'раздел',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        verbose_name=u'категория',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    type = models.IntegerField(
        verbose_name=u'тип блока',
        default=0,
        choices=CATALOG_ITEM_TYPES
    )
    order_key = models.PositiveIntegerField(
        verbose_name=u'',
        default=0,
        blank=False,
        null=False
    )

    @property
    def catalog_item(self):
        return self.section or self.category

    def clean(self):
        super().clean()
        if bool(self.section) == bool(self.category):
            raise ValidationError(u'Выберите либо раздел, либо категорию.')

    def __str__(self):
        return str(self.catalog_item or '')