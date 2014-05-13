# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0006_auto_20140512_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorship',
            name='level',
            field=models.IntegerField(null=True, choices=[(10, 'Platinum'), (20, 'Gold'), (30, 'Silver'), (40, 'Indies')], help_text='Sponsorship level (if applicable)', blank=True),
            preserve_default=True,
        ),
    ]
