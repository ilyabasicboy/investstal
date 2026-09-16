# -*- encoding: utf-8 -*-
from mptt.signals import node_moved
from django.db.models.signals import post_save, pre_delete
from django.db import transaction
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from catalog.models import TreeItem
from investstal.content_generator.models import ContentTemplate
from investstal.custom_catalog.models import Category, Section, Product, Thermal


def catalog_changed_handler(sender, instance, **kwargs):

    """ Логика очистки кэша после изменения каталога """

    cache.clear()


post_save.connect(catalog_changed_handler, sender=Section)
post_save.connect(catalog_changed_handler, sender=Product)
post_save.connect(catalog_changed_handler, sender=Category)
post_save.connect(catalog_changed_handler, sender=Thermal)
pre_delete.connect(catalog_changed_handler, sender=Section)
pre_delete.connect(catalog_changed_handler, sender=Product)
pre_delete.connect(catalog_changed_handler, sender=Category)
pre_delete.connect(catalog_changed_handler, sender=Thermal)
node_moved.connect(catalog_changed_handler, sender=TreeItem)


@receiver(post_save, sender=Product)
@receiver(post_save, sender=Section)
@receiver(post_save, sender=Thermal)
def update_parameters(sender, instance, created, **kwargs):
    """Обновляет наследуемые параметры товаров после сохранения товара, раздела или термодвери."""
    if isinstance(instance, Product):
        transaction.on_commit(lambda: instance.update_parameters())
        if created:
            transaction.on_commit(lambda: process_product_creation(instance))
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
    elif isinstance(instance, Thermal):
        def update_all_products():
            for product in instance.product_set.all():
                product.update_parameters()

        transaction.on_commit(update_all_products)


def process_product_creation(product):
    """Создает SEO-тексты товара из шаблона родительского раздела."""
    try:
        parent = product.tree.get().parent.content_object
        ct = ContentType.objects.get_for_model(parent)
        content_template = ContentTemplate.objects.filter(object_id=parent.id, content_type=ct).first()
        if content_template and content_template.autogen and (
                content_template.title or content_template.description or content_template.keywords):
            child_models = content_template.get_child_models()
            if product.__class__.__name__.lower() in child_models:
                content_template.apply_text_for_item(product)
    except Exception:
        pass
