# -*- coding: utf-8 -*-
from django import forms
from django.core.mail.message import EmailMessage
from feedback.forms import BaseFeedbackForm
from nocaptcha_recaptcha.fields import NoReCaptchaField


class BaseForm(BaseFeedbackForm):

    ERROR_MESSAGES = {
        'required': u'Заполните поле',
        'invalid': u'Неправильное значение'
    }

    def after_mail(self, **kwargs):

        """ Дополнительная логика после отправки письма
            данные данные формы доступны через self """
        pass

    def __init__(self, *args, **kwargs):

        """ Указание начальных данных формы, например переопределит тексты ошибок """

        super(BaseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].error_messages = self.ERROR_MESSAGES

    captcha = NoReCaptchaField(label='')


class CallForm(BaseForm):

    """ Тестовая форма
        аттрибут data-set применять для разделения полей формы по группам
        Пример вывода группы полей в шаблоне:
    """

    name = forms.CharField(
        label=u'Ф.И.О.',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    email = forms.EmailField(
        label=u'Адрес электронной почты',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    phone = forms.CharField(
        label=u'Контактный телефон:', required=False,
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    message = forms.CharField(
        label=u'Сообщение:', max_length=1000,
        widget=forms.Textarea(attrs={'data-set': 2}),
    )
