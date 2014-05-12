# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0004_auto_20140512_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='logo_url',
            field=models.URLField(blank=True, help_text='URL to download logo from instead of direct upload.', max_length=500, null=True),
            preserve_default=True,
        ),
    ]
