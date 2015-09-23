# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0005_auto_20150918_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancer',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
