# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0022_auto_20151203_2309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gene',
            old_name='locus',
            new_name='locus_begin',
        ),
        migrations.AddField(
            model_name='gene',
            name='locus_end',
            field=models.IntegerField(null=True),
        ),
    ]
