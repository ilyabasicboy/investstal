# -*- coding: utf-8 -*-
from .utils.parser import TextGenerator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from catalog.utils import get_content_objects
from catalog.models import CatalogBase
import re
from django.utils.encoding import smart_str
from seo.models import Seo


class ContentTemplate(models.Model):

    class Meta:
        verbose_name = u"Шаблон контента"
        verbose_name_plural = u"Шаблоны контента"

    title = models.TextField(
        verbose_name=u"Заголовок",
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name=u"Описание",
        null=True, blank=True
    )
    keywords = models.TextField(
        verbose_name=u"Ключевые слова",
        null=True, blank=True
    )
    title_length = models.PositiveIntegerField(
        verbose_name=u"max символов заголовка",
        default=0
    )
    description_length = models.PositiveIntegerField(
        verbose_name=u"max символов описания",
        default=0
    )
    keywords_length = models.PositiveIntegerField(
        verbose_name=u"max символов ключевые слова",
        default=0
    )
    autogen = models.BooleanField(
        verbose_name=u'автогенерация текста для новых товаров',
        default=True
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_child_models(self):
        """
            Возвращает список строк с названиями моделей,
            для которых нужно сгенерировать контент.
        """

        child_models = []

        for obj in settings.CONTENT_FOR_MODELS:
            if obj["model"]["name"] == self.content_object.__class__.__name__:
                for child_model in obj["allowed_child_models"]:
                    child_models += [child_model['name'].lower()]

        return child_models

    def get_children(self):

        """ Возвращает list дочерних объектов для генерации контента """

        child_models = self.get_child_models()

        if isinstance(self.content_object, CatalogBase):
            children = get_content_objects(
                self.content_object.tree.get().get_descendants().filter(
                    content_type__model__in=child_models
                ),
                show=False
            )
        else:
            children = self.content_object.get_descendants().filter(
                    content_type__model__in=child_models
                )

        return children

    def get_object_seo(self, instance):

        """ Возвращает название поля объекта, генерации контента """

        for obj in settings.CONTENT_FOR_MODELS:
            if obj["model"]["name"] == self.content_object.__class__.__name__:
                for child_model in obj["allowed_child_models"]:
                    if child_model['name'] == instance.__class__.__name__:
                        ct = ContentType.objects.get_for_model(instance)
                        seo = Seo.objects.filter(content_type=ct, object_id=instance.id).first()
                        if not seo:
                            seo = Seo.objects.create(content_type=ct, object_id=instance.id)
                        return seo

        return None

    def set_field_values_in_text(self, instance, text):
        """
        Вставляет значения волей объекта в текст.
        Если такого поля нет, либо поле не заполнено,
        заполнится "".
        """

        fields = re.findall(r"(#([\w\-_]+)#)", text)

        for field in fields:
            # Если в конце названия есть окончание '__st', привести значение к нижнему регистру
            if re.search(r'__st$', field[1]):
                value = getattr(instance,  re.sub('__st', '', field[1]), u'')
                if callable(value):
                    value = value()
                if value:
                    value = smart_str(value)
                    value_list = list(value)
                    value_list[0] = value_list[0].lower()
                    value = ''.join(value_list)
                else:
                    value = u''
            elif re.search(r'__parameter$', field[1]):
                parameter_slug = re.sub('__parameter', '', field[1])
                parameter_inline = instance.parameters.filter(parameter_group__slug=parameter_slug).exclude(value=None).first()
                if parameter_inline:
                    value = parameter_inline.value
                else:
                    value = u''
                value = smart_str(value)
            else:
                value = getattr(instance, field[1], u'')
                if callable(value):
                    value = value()
                if not value:
                    value = u''
                value = smart_str(value)

            text = re.sub(field[0], value, text)

        return text

    def apply_text_for_item(self, item):

        """ Используется при создании нового дочернего объекта """

        title_generator = TextGenerator(self.title)
        desc_generator = TextGenerator(self.description)
        keywords_generator = TextGenerator(self.keywords)

        seo = self.get_object_seo(item)
        title = next(title_generator.generate_textlist())
        description = next(desc_generator.generate_textlist())
        keywords = next(keywords_generator.generate_textlist())

        # Заменить названия полей в тексте на их значения
        replaced_title = self.set_field_values_in_text(item, title)
        replaced_description = self.set_field_values_in_text(item, description)
        replaced_keywords = self.set_field_values_in_text(item, keywords)

        if seo:

            if self.title_length or self.description_length or self.keywords_length:
                title_length = len(replaced_title)
                description_length = len(replaced_description)
                keywords_length = len(replaced_keywords)
                if self.title_length and self.title_length < title_length:
                    replaced_title = replaced_title[:self.title_length] + '...'
                if self.description_length and self.description_length < description_length:
                    replaced_description = replaced_description[:self.description_length] + '...'
                if self.keywords_length and self.keywords_length < keywords_length:
                    replaced_keywords = replaced_keywords[:self.keywords_length] + '...'

            seo.title = replaced_title
            seo.description = replaced_description
            seo.keywords = replaced_keywords

            seo.save()


    def apply_text(self, apply_types=0, title_length=0, description_length=0, keywords_length=0, title=None, description=None, keywords=None):

        """ Применить текст к дочерним объектам """

        if self.title:

            children = self.get_children()

            if not title:
                title = self.title
            if not description:
                description = self.description
            if not keywords:
                keywords = self.keywords

            title_generator = TextGenerator(title)
            desc_generator = TextGenerator(description)
            keywords_generator = TextGenerator(keywords)

            for child in children:
                seo = self.get_object_seo(child)

                # При каждой итерации генерируется рандомный текст
                title = next(title_generator.generate_textlist())
                description = next(desc_generator.generate_textlist())
                keywords = next(keywords_generator.generate_textlist())

                # Заменить названия полей в тексте на их значения
                replaced_title = self.set_field_values_in_text(child, title)
                replaced_description = self.set_field_values_in_text(child, description)
                replaced_keywords = self.set_field_values_in_text(child, keywords)

                if seo:

                    title_text_length = len(replaced_title)
                    description_text_length = len(replaced_description)
                    keywords_text_length = len(replaced_keywords)

                    if title_length or description_length or keywords_length:
                        if title_length and title_length < title_text_length:
                            replaced_title = replaced_title[:title_length] + '...'
                        if description_length and description_length < description_text_length:
                            replaced_description = replaced_description[:description_length] + '...'
                        if keywords_length and keywords_length < keywords_text_length:
                            replaced_keywords = replaced_keywords[:keywords_length] + '...'

                    if apply_types == 1 or not seo.title:
                        seo.title = replaced_title
                    if apply_types == 1 or not seo.description:
                        seo.description = replaced_description
                    if apply_types == 1 or not seo.keywords:
                        seo.keywords = replaced_keywords

                    seo.save()

    def clear_texts(self):
        children = self.get_children()

        for child in children:
            ct = ContentType.objects.get_for_model(child)
            seo = Seo.objects.filter(content_type=ct, object_id=child.id).delete()
