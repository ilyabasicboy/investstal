# -*- coding: utf-8 -*-
# from django.db.models.signals import post_save, pre_delete
# from django.core.cache import cache
# from pages.models import Page
# from mptt.signals import node_moved
#
#
# def page_changed_handler(sender, instance, **kwargs):
#
#     """ Очистка кэша страниц при необходимости """
#
#     cache.clear()
#
# post_save.connect(page_changed_handler, sender=Page)
# pre_delete.connect(page_changed_handler, sender=Page)
# node_moved.connect(page_changed_handler, sender=Page)
