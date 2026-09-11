# Generated manually from titan parameter logic

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('custom_catalog', '0003_auto_20260911_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_key', models.PositiveIntegerField(default=0, verbose_name='')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, help_text='Используется в генераторе метатегов', null=True, unique=True, verbose_name='slug')),
                ('type', models.IntegerField(blank=True, choices=[(1, 'Стандартная конструкция'), (2, 'Фурнитура'), (3, 'Базовые габариты двери'), (4, 'Доставка дверей'), (5, 'Установка дверей')], help_text='Используется на странице товара для деления в характеристиках', null=True, verbose_name='Тип параметра')),
            ],
            options={
                'verbose_name': 'группа параметра',
                'verbose_name_plural': 'группы параметров',
                'ordering': ['order_key'],
            },
        ),
        migrations.CreateModel(
            name='ParameterValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(max_length=255, verbose_name='Значение')),
                ('link_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='текст ссылки')),
                ('size_type', models.PositiveIntegerField(blank=True, choices=[(1, 'Однопольная'), (2, 'Двупольная')], help_text='Заполнять только для параметра "Размер по коробке"', null=True, verbose_name='Тип конструкции "Размер по коробке"')),
                ('show_images', models.BooleanField(default=False, verbose_name='Выгружать фото на страницу товара')),
                ('show_in_additional_choices', models.BooleanField(default=False, verbose_name='добавляется в админке в выборе доп.параметров')),
                ('extra_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='дополнительная наценка товара')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.Page', verbose_name='ссылка на страницу')),
                ('parameter_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_catalog.ParameterGroup', verbose_name='Название параметра')),
            ],
            options={
                'verbose_name': 'значение параметра',
                'verbose_name_plural': 'значения параметров',
            },
        ),
        migrations.CreateModel(
            name='ParameterInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_catalog.ParameterGroup', verbose_name='Название')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_parameters', to='custom_catalog.Product')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_parameters', to='custom_catalog.Section')),
                ('value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_catalog.ParameterValue', verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'добавить параметр',
                'verbose_name_plural': 'добавить параметры',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='parameters',
            field=models.ManyToManyField(blank=True, help_text='Суммарные параметры, наследуемые от разделов и подразделов. Логика в сигналах.', related_name='products', to='custom_catalog.ParameterValue', verbose_name='Параметры'),
        ),
    ]
