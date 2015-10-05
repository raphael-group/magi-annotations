# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0012_auto_20150922_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='cancer',
            field=models.ForeignKey(to='annotations.Cancer', blank=True),
        ),
    ]
