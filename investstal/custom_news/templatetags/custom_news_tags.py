# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from easy_news.models import News
from attachment.models import AttachmentImage
from investstal.custom_news.models import NewsRoot

try:
    NEWS_CT = ContentType.objects.get_for_model(News)
except:
    pass

register = template.Library()


@register.inclusion_tag('easy_news/parts/block_cards.html', takes_context=True)
def show_block_news(context):

    """ Отображает блок новостей """

    context['object_list'] = []
    for obj in News.objects.filter(show=True):
        context['object_list'].append({
            'title': obj.title,
            'date': obj.date,
            'short_description': obj.short_description,
            'get_absolute_url': obj.get_absolute_url(),
            'image': AttachmentImage.objects
                .filter(object_id=obj.id, content_type=NEWS_CT).first()
        })
    return context


@register.simple_tag()
def get_news_root():

    """ Возвращает корневую новостей """

    return NewsRoot.objects.all().first()