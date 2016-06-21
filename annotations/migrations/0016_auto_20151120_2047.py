# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0015_gene_interaction_interactionreference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interactionreference',
            name='identifier',
            field=models.CharField(max_length=40),
        ),
    ]
