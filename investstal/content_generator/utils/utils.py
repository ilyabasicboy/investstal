# -*- coding: utf-8 -*-
from django.apps import apps as django_apps
from django.conf import settings


def get_content_models():
    """
    Generator for list of registered models in seogen
    """
    CONTENT_FOR_MODELS = getattr(settings, 'CONTENT_FOR_MODELS', [])

    for pair in CONTENT_FOR_MODELS:
        app_name = pair["model"]["app_name"]
        model_name = pair["model"]["name"]
        yield django_apps.get_model(app_name, model_name)
