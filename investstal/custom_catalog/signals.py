# -*- encoding: utf-8 -*-
from mptt.signals import node_moved
from django.db.models.signals import post_save, pre_delete
from django.db import transaction
from django.dispatch import receiver
from django.core.cache import cache
from catalog.models import TreeItem
from investstal.custom_catalog.models import Category, Section, Product


def catalog_changed_handler(sender, instance, **kwargs):

    """ Логика очистки кэша после изменения каталога """

    cache.clear()


post_save.connect(catalog_changed_handler, sender=Section)
post_save.connect(catalog_changed_handler, sender=Product)
post_save.connect(catalog_changed_handler, sender=Category)
pre_delete.connect(catalog_changed_handler, sender=Section)
pre_delete.connect(catalog_changed_handler, sender=Product)
pre_delete.connect(catalog_changed_handler, sender=Category)
node_moved.connect(catalog_changed_handler, sender=TreeItem)


@receiver(post_save, sender=Product)
@receiver(post_save, sender=Section)
def update_parameters(sender, instance, created, **kwargs):
    """Обновляет наследуемые параметры товаров после сохранения товара или раздела."""
    if isinstance(instance, Product):
        transaction.on_commit(lambda: instance.update_parameters())
    elif isinstance(instance, Section):
        def update_all_products():
            try:
                product_ids = instance.tree.get().get_descendants().filter(
                    content_type__model='product'
                ).values_list('object_id', flat=True)
                products = Product.objects.filter(id__in=product_ids)
            except:
                products = instance.get_products()

            for product in products:
                product.update_parameters()

        transaction.on_commit(update_all_products)
