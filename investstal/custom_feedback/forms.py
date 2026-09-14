# -*- coding: utf-8 -*-
from django import forms
from django.core.mail.message import EmailMessage
from feedback.forms import BaseFeedbackForm
from django.core.exceptions import ValidationError


def validate_is_human(value):
    if value != 'on':
        raise forms.ValidationError(':(')
    return value


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError(u"Максимальный размер файла 5 мб")
    else:
        return value


class BaseForm(BaseFeedbackForm):

    ERROR_MESSAGES = {
        'required': u'Заполните поле',
        'invalid': u'Неправильное значение'
    }

    confirm = forms.BooleanField(
        label=u'Согласие на обработку',
        required=True,
        initial=True
    )

    flag = forms.CharField(
        label=u'Флаг',
        required=False,
        widget=forms.widgets.HiddenInput,
        initial='none',
        validators=[validate_is_human],
    )

    def after_mail(self, **kwargs):

        """ Дополнительная логика после отправки письма
            данные данные формы доступны через self """
        pass

    def __init__(self, *args, **kwargs):

        """ Указание начальных данных формы, например переопределит тексты ошибок """

        super(BaseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].error_messages = self.ERROR_MESSAGES


class BaseFileForm(forms.Form):

    file = forms.FileField(
        label=u'Прикрепить файл',
        validators=[validate_file_size],
        required=False,
        help_text=u'Допустимо: JPG, PNG, PDF до 5 Мб',
        widget=forms.FileInput(
            attrs={
                'data-accept-imgfile': '',
            }
        )
    )

    def mail(self, request):

        message = self.render_message(request)
        headers = {}
        if 'email' in self.cleaned_data:
            headers = {'Reply-to': self.cleaned_data.get('email')}

        msg = EmailMessage(self.subject, message, self.sender, self.recipients, headers=headers)
        if request.FILES:
            files_copy = dict(request.FILES)
            uploaded_files = files_copy
            for uploaded_file in uploaded_files['file']:  # file is the name value which you have provided in form for file field
                msg.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        msg.send()
        self.after_mail(message=message, headers=headers)


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


class Consult(BaseForm):

    """
        Консультация
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ваше имя'
            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ваш телефон'
            }
        ),
    )


class Rackman(BaseFileForm, BaseForm):

    """
        Вызвать замерщика
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ваше имя'
            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )
    email = forms.EmailField(
        label=u'E-mail:',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Ваш e-mail'
            }
        ),
    )
    date_call = forms.CharField(
        label=u'Дата замера:',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Дата'
            }
        ),
    )
    time_call = forms.CharField(
        label=u'Желаемое время:',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Время'
            }
        ),
    )
    comment = forms.CharField(
        label=u'Комментарий менеджеру:',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Комментарий менеджеру'
            }
        ),
    )