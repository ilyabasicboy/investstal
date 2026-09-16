# -*- coding:utf-8 -*-
from django.apps import AppConfig


class ContentGeneratorAppConfig(AppConfig):
    name = 'investstal.content_generator'

    def ready(self):
        import investstal.content_generator.signals
        pass
