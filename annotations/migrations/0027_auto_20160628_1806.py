# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0026_auto_20151210_2059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cancer',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='annotation',
            name='characterization',
            field=models.CharField(blank=True, max_length=20, choices=[(b'F', b'Functional'), (b'O', b'Observational'), (b'', b'Unknown')]),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='heritable',
            field=models.CharField(blank=True, max_length=8, verbose_name=b'Heritability', choices=[(b'G', b'Germline'), (b'S', b'Somatic'), (b'', b'Unknown')]),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='measurement_type',
            field=models.CharField(blank=True, max_length=30, choices=[(b'WXS', b'Whole-Exome Sequencing'), (b'WGS', b'Whole-Genome Sequencing'), (b'TS', b'Targeted Sequencing'), (b'', b'Unknown')]),
        ),
    ]
