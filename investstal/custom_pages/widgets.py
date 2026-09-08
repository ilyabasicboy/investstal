# -*- coding: utf-8 -*-
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Select, CheckboxInput, Textarea
from pages.models import Page
from pages.widgets_registry import register_widget
from tinymce.widgets import TinyMCE

register_widget(TinyMCE)


class LargeTextarea(Textarea):

    def __init__(self, language=None, attrs=None, **kwargs):
        attrs = {'cols': None}
        super(LargeTextarea, self).__init__(attrs)


register_widget(LargeTextarea)


class Checkbox(CheckboxInput):

    def __init__(self, language=None, attrs=None, **kwargs):
        attrs = {'style': 'display:inline-block;margin:6px 3px 3px 4px;'}
        super(Checkbox, self).__init__(attrs)
        self.check_test = self.check

    def check(self, value):
        if value in [None, False, '', 'False']:
            return False
        else:
            return bool(value)

    def value_from_datadict(self, data, files, name):
        return name in data


class GallerySelect(Select):

    def __init__(self, language=None, attrs=None, **kwargs):
        super(GallerySelect, self).__init__(attrs)
        groups = Page.objects.filter(status=Page.PUBLISHED, template='pages/gallery.html')
        choices = [('', u'-----------')] + [(group.id, group.title()) for group in groups]
        self.choices = list(choices)


class MultiSelect(FilteredSelectMultiple):

    def __init__(self, language=None, attrs=None, **kwargs):
        super(MultiSelect, self).__init__(language, attrs, **kwargs)
        pages = Page.objects.filter(status=Page.PUBLISHED, template='pages/default.html')
        self.choices = list(((page.id, page.title()) for page in pages))

    def render(self, name, value, attrs=None, **kwargs):
        self.verbose_name = u'Страницы'
        self.is_stacked = False
        if value:
            value = value[1:len(value) - 1].split(',')
            value = [int(id.strip()) for id in value]
        rendered = super(MultiSelect, self).render(name, value, attrs, **kwargs)
        return rendered

    def render_options(self, choices, selected_choices):
        if isinstance(selected_choices, basestring):
            selected_choices = selected_choices[1:-1]
            selected_choices = [s[2:-1] for s in selected_choices.split(', ')]
        return super(MultiSelect, self).render_options(choices, selected_choices)

    def value_from_datadict(self, data, files, name):
        return [int(str_id) for str_id in data.getlist(name)]


register_widget(Checkbox)
register_widget(GallerySelect)
register_widget(MultiSelect)
