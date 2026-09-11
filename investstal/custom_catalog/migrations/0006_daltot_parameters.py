# Generated manually from daltot parameter logic

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_catalog', '0005_auto_20260911_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parametergroup',
            old_name='type',
            new_name='group_type',
        ),
        migrations.AlterField(
            model_name='parametergroup',
            name='group_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Стандартные параметры'), (2, 'Размеры двери'), (3, 'Доставка дверей'), (4, 'Открывание'), (5, 'Отделки')], help_text='Используется на странице товара для деления в характеристиках', null=True, verbose_name='Тип параметра'),
        ),
        migrations.AddField(
            model_name='parametergroup',
            name='round_images',
            field=models.BooleanField(default=False, verbose_name='Показывать отделки в виде круга'),
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='short_description',
            field=models.TextField(blank=True, null=True, verbose_name='краткое описание'),
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='полное описание'),
        ),
        migrations.RemoveField(
            model_name='parametervalue',
            name='size_type',
        ),
        migrations.CreateModel(
            name='Thermal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='название')),
            ],
            options={
                'verbose_name': 'Термодверь',
                'verbose_name_plural': 'Термодвери',
            },
        ),
        migrations.AddField(
            model_name='parameterinline',
            name='thermal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thermal_parameters', to='custom_catalog.Thermal'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='custom_catalog.Thermal', verbose_name='Термодверь'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_content',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Описание товара'),
        ),
    ]
