# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0008_auto_20140513_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='When this was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='When this was last modified.')),
                ('published', models.DateTimeField(help_text="When to publish this (this can be in the future). Note that you'll need to tick the public flag too.")),
                ('gamecraft', models.ForeignKey(null=True, to_field='id', on_delete=django.db.models.deletion.SET_NULL, to='gamecrafts.GameCraft', blank=True, help_text='If this relates to a particular gamecraft use this.')),
                ('slug', models.SlugField(max_length=600, help_text='Short name in url, hopefully automatically populated :) e.g. 2014-04-03-london-gamecraft-2014')),
                ('title', models.CharField(max_length=500, unique=True, help_text='Title of news post')),
                ('content', models.TextField(blank=True, help_text='The news article, in Markdown.')),
                ('public', models.BooleanField(help_text='Set to True to make visible generally, otherwise you need the specific link.', default=False)),
            ],
            options={
                'permissions': (('modify_gamecraft', 'Can create, edit and delete a GameCraft'),),
                'ordering': ['published', 'slug', 'title', 'modified', 'created'],
                'unique_together': set([('published', 'slug')]),
                'verbose_name_plural': 'news',
            },
            bases=(models.Model,),
        ),
    ]
