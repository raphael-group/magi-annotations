# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0007_auto_20150921_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mutation',
            name='new_amino_acid',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='mutation',
            name='original_amino_acid',
            field=models.CharField(max_length=30),
        ),
    ]
