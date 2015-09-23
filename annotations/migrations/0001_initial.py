# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heritable', models.CharField(max_length=8, choices=[(b'G', b'Germline'), (b'S', b'Somatic')])),
                ('measurement_type', models.CharField(max_length=30, choices=[(b'WXS', b'Whole-Exome Sequencing'), (b'WGS', b'Whole-Genome Sequencing'), (b'TS', b'Targeted Sequencing')])),
                ('characterization', models.CharField(max_length=20, choices=[(b'F', b'Functional'), (b'O', b'Observational')])),
                ('comment', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Cancer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Mutation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gene', models.CharField(max_length=30)),
                ('locus', models.IntegerField(verbose_name=b'locus')),
                ('original_amino_acid', models.CharField(max_length=5)),
                ('new_amino_acid', models.CharField(max_length=5)),
                ('mutation_type', models.CharField(max_length=15, choices=[(b'MS', b'Missense'), (b'NS', b'Nonsense')])),
                ('mutation_class', models.CharField(max_length=15, choices=[(b'SNV', b'Single Nucleotide Variant'), (b'indel', b'Small insertion/deletion')])),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=30)),
                ('db', models.CharField(max_length=30, choices=[(b'PMID', b'PubMed'), (b'PMC', b'PubMed Central')])),
                ('source', models.CharField(max_length=30, choices=[(b'C', b'Community'), (b'DoCM', b'Database of Curated Mutations'), (b'PMC Search', b'PubMed Central Search')])),
                ('mutation', models.ForeignKey(to='annotations.Mutation')),
            ],
        ),
        migrations.AddField(
            model_name='annotation',
            name='cancers',
            field=models.ManyToManyField(to='annotations.Cancer'),
        ),
    ]
