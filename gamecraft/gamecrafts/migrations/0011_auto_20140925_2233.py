# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0010_auto_20140619_2351'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-published', 'slug', 'title', '-modified', '-created'], 'permissions': (('modify_gamecraft', 'Can create, edit and delete a GameCraft'),), 'verbose_name_plural': 'news'},
        ),
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['name', 'modified'], 'permissions': (('modify_gamecraft', 'Can create, edit and delete a GameCraft'),)},
        ),
        migrations.AlterModelOptions(
            name='sponsorship',
            options={'ordering': ['level', '-starts', 'modified'], 'permissions': (('modify_gamecraft', 'Can create, edit and delete a GameCraft'),)},
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='level',
            field=models.IntegerField(choices=[(10, 'Platinum'), (20, 'Gold'), (30, 'Silver'), (40, 'Indies'), (50, 'Partner'), (60, 'Media Partner')], blank=True, help_text='Sponsorship level (if applicable)', null=True),
        ),
    ]
