# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0009_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='published',
            field=models.DateTimeField(help_text="When to publish this (this can be in the future). Note that you'll need to tick the public flag too. This also controls the URL."),
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=600, help_text='Short name in url, hopefully automatically populated :) e.g. news-post'),
        ),
    ]
