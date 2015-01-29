# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamecrafts', '0013_auto_20150128_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='logo',
        ),
    ]
