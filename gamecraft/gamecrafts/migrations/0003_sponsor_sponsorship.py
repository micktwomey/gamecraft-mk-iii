# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0002_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='When this was created.', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text='When this was last modified.', auto_now=True)),
                ('slug', models.SlugField(help_text='Short name of sponsor.', max_length=500)),
                ('name', models.CharField(unique=True, help_text='Name of sponsor.', max_length=500)),
                ('url', models.URLField(help_text="URL of sponsor's site.", max_length=500)),
                ('logo', models.ImageField(upload_to='gamecraft/sponsors/%Y/%m/%d', help_text='The image used for the sponsor logo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reated', models.DateTimeField(help_text='When this was created.', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text='When this was last modified.', auto_now=True)),
                ('sponsor', models.ForeignKey(to='gamecrafts.Sponsor', to_field='id')),
                ('description', models.TextField(help_text="Optional blurb about this sponsorship (Markdown). Most likely won't get used yet :)", blank=True)),
                ('starts', models.DateTimeField(help_text='The time the sponsorship starts.')),
                ('ends', models.DateTimeField(help_text='The time the sponsorship ends.')),
                ('gamecraft', models.ForeignKey(to='gamecrafts.GameCraft', on_delete=django.db.models.deletion.SET_NULL, null=True, help_text='If this is a single event sponsor then use this. Conflicts with starts and ends.', blank=True, to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
