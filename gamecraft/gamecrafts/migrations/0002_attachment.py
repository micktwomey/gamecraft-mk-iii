# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(help_text='When this was created.', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text='When this was last modified.', auto_now=True)),
                ('comment', models.TextField(help_text='Optional comment on the image (Markdown encouraged).', blank=True)),
                ('attachment', models.FileField(blank=True, upload_to='gamecraft/attachments/%Y/%m/%d')),
                ('url', models.CharField(help_text='URL to fetch file from', blank=True, max_length=1000)),
                ('gamecraft', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', to='gamecrafts.GameCraft')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
