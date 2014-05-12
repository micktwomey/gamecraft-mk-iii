# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0005_sponsor_logo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ImageField(null=True, blank=True, help_text='The image used for the sponsor logo', upload_to='gamecraft/sponsors/%Y/%m/%d'),
        ),
    ]
