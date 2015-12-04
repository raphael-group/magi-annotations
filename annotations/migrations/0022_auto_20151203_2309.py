# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0021_interactionreference_db'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mutation',
            name='gene',
            field=models.ForeignKey(to='annotations.Gene'),
        ),
    ]
