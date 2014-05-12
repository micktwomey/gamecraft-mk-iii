# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0003_sponsor_sponsorship'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsorship',
            old_name='reated',
            new_name='created',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
    ]
