# Generated manually for catalog filtering controls.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_catalog', '0007_auto_20260915_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='category',
            name='hide_filter_category',
            field=models.BooleanField(default=False, verbose_name='скрыть фильтр по категориям'),
        ),
        migrations.AddField(
            model_name='category',
            name='show_on_filter',
            field=models.BooleanField(default=True, verbose_name='отображать в фильтре'),
        ),
        migrations.AddField(
            model_name='section',
            name='hide_filter_category',
            field=models.BooleanField(default=False, verbose_name='скрыть фильтр по категориям'),
        ),
        migrations.AddField(
            model_name='section',
            name='show_on_filter',
            field=models.BooleanField(default=True, verbose_name='отображать в фильтре'),
        ),
        migrations.AddField(
            model_name='category',
            name='filter_exclude_category',
            field=models.ManyToManyField(blank=True, limit_choices_to={'show_on_filter': True}, related_name='+', to='custom_catalog.Category', verbose_name='категории, исключенные из вывода в фильтр'),
        ),
        migrations.AddField(
            model_name='category',
            name='filter_exclude_section',
            field=models.ManyToManyField(blank=True, limit_choices_to={'show_on_filter': True}, related_name='+', to='custom_catalog.Section', verbose_name='разделы, исключенные из вывода в фильтр'),
        ),
        migrations.AddField(
            model_name='section',
            name='filter_exclude_category',
            field=models.ManyToManyField(blank=True, limit_choices_to={'show_on_filter': True}, related_name='+', to='custom_catalog.Category', verbose_name='категории, исключенные из вывода в фильтр'),
        ),
        migrations.AddField(
            model_name='section',
            name='filter_exclude_section',
            field=models.ManyToManyField(blank=True, limit_choices_to={'show_on_filter': True}, related_name='+', to='custom_catalog.Section', verbose_name='разделы, исключенные из вывода в фильтр'),
        ),
    ]
