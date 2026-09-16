# -*- coding: utf-8 -*-
from django import forms
from .models import ContentTemplate

APPLY_TYPES = (
    (0, u'Свободным'),
    (1, u'Всем'),
)


class ContentTemplateAdminForm(forms.ModelForm):

    class Meta:
        model = ContentTemplate
        fields = '__all__'

    generate = forms.BooleanField(
        label=u'Сгенерировать тексты',
        required=False
    )
    apply_types = forms.ChoiceField(
        label=u'Сгенерировать',
        choices=APPLY_TYPES,
        initial=0,
        widget=forms.RadioSelect(),
        required=False
    )
    clear_texts = forms.BooleanField(
        label=u'Очистить тексты',
        required=False
    )

    def save(self, *args, **kwargs):

        super(ContentTemplateAdminForm, self).save(*args, **kwargs)

        """ Работает при повторном сохранении шаблона """
        generate = self.cleaned_data.get('generate')
        apply_types = int(self.cleaned_data.get('apply_types', '0'))
        clear_texts = self.cleaned_data.get('clear_texts')
        instance = self.cleaned_data.get('id')
        title_length = int(self.cleaned_data.get('title_length', '0'))
        description_length = int(self.cleaned_data.get('description_length', '0'))
        keywords_length = int(self.cleaned_data.get('keywords_length', '0'))
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        keywords = self.cleaned_data.get('keywords')

        if instance:
            if clear_texts:
                instance.clear_texts()
            elif generate:
                instance.apply_text(apply_types, title_length, description_length, keywords_length, title, description, keywords)
