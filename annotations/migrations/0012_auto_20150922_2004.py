# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0011_auto_20150922_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='cancer',
            field=models.ForeignKey(blank=True, to='annotations.Cancer', null=True),
        ),
    ]
