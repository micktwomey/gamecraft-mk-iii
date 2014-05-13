# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0007_sponsorship_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='starts',
            field=models.DateTimeField(null=True, help_text='The time the sponsorship starts.', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='ends',
            field=models.DateTimeField(null=True, help_text='The time the sponsorship ends.', blank=True),
        ),
    ]
