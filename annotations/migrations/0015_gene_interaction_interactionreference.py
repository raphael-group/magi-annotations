# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0014_auto_20150924_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('chromosome', models.SmallIntegerField(null=True)),
                ('locus', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('input_source', models.CharField(max_length=25)),
                ('source', models.ForeignKey(related_name='source', to='annotations.Gene')),
                ('target', models.ForeignKey(related_name='target', to='annotations.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='InteractionReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=20)),
                ('interaction', models.ForeignKey(to='annotations.Interaction')),
            ],
        ),
    ]
