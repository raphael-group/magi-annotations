# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0014_auto_20150924_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='heritable',
            field=models.CharField(blank=True, max_length=8, verbose_name=b'Heritability', choices=[(b'G', b'Germline'), (b'S', b'Somatic')]),
        ),
        migrations.AlterUniqueTogether(
            name='mutation',
            unique_together=set([('gene', 'locus', 'original_amino_acid', 'new_amino_acid', 'mutation_type', 'mutation_class')]),
        ),
        migrations.AlterUniqueTogether(
            name='reference',
            unique_together=set([('identifier', 'db', 'mutation')]),
        ),
    ]
