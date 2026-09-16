# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from investstal.content_generator.models import ContentTemplate
from investstal.content_generator.utils.utils import get_content_models
from investstal.content_generator.forms import ContentTemplateAdminForm
from django.contrib.contenttypes.models import ContentType


class ContentTemplateInline(GenericStackedInline):
    model = ContentTemplate
    extra = 0
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            ct = ContentType.objects.get_for_model(obj)
            content_template = ContentTemplate.objects.filter(content_type=ct, object_id=obj.id).first()

            # Изменить форму, если шаблон уже существует
            if content_template:
               self.form = ContentTemplateAdminForm
        return super(ContentTemplateInline, self).get_formset(request, obj, **kwargs)


for model in get_content_models():
    model_admin = admin.site._registry[model].__class__
    admin.site.unregister(model)

    setattr(model_admin, 'inlines', getattr(model_admin, 'inlines', []))
    if not ContentTemplateInline in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [ContentTemplateInline]

    admin.site.register(model, model_admin)
