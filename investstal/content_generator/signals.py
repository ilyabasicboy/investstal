# -*- coding:utf-8 -*-
from catalog.signals import content_object_created
from django.contrib.contenttypes.models import ContentType
from investstal.content_generator.models import ContentTemplate
from django.db.models.signals import post_save
from django.conf import settings


CONTENT_MODELS = [obj['model']['name'].lower() for obj in settings.CONTENT_FOR_MODELS]


def item_created_handler(sender, instance, parent, **kwargs):

    """ Заполнить контент при создании элемента каталога """

    ct = ContentType.objects.get_for_model(parent)
    if ct.model in CONTENT_MODELS:
        content_template = ContentTemplate.objects.filter(object_id=parent.id, content_type=ct).first()
        if content_template and content_template.autogen and (content_template.title or content_template.description or content_template.keywords):
            child_models = content_template.get_child_models()
            if instance.__class__.__name__.lower() in child_models:
                content_template.apply_text_for_item(instance)


# content_object_created.connect(item_created_handler)


def content_model_saved(sender, instance, raw, created, **kwargs):

    """" Применить тексты при создании шаблона """

    if created:
        instance.apply_text(
            title_length=instance.title_length,
            description_length=instance.description_length,
            keywords_length=instance.keywords_length
        )


post_save.connect(content_model_saved, sender=ContentTemplate)
