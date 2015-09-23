# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0008_auto_20150921_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='cancer',
            field=models.ForeignKey(to='annotations.Cancer', blank=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='characterization',
            field=models.CharField(blank=True, max_length=20, choices=[(b'F', b'Functional'), (b'O', b'Observational')]),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='comment',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='heritable',
            field=models.CharField(blank=True, max_length=8, choices=[(b'G', b'Germline'), (b'S', b'Somatic')]),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='measurement_type',
            field=models.CharField(blank=True, max_length=30, choices=[(b'WXS', b'Whole-Exome Sequencing'), (b'WGS', b'Whole-Genome Sequencing'), (b'TS', b'Targeted Sequencing')]),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
