# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0023_auto_20151204_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gene',
            name='chromosome',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
