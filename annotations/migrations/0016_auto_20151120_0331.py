# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0015_auto_20151119_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancer',
            name='id',
        ),
        migrations.AlterField(
            model_name='cancer',
            name='abbr',
            field=models.CharField(max_length=10, serialize=False, primary_key=True),
        ),
    ]
