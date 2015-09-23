# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0002_annotation_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='cancers',
        ),
        migrations.AddField(
            model_name='annotation',
            name='cancer',
            field=models.ForeignKey(default='', to='annotations.Cancer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mutation',
            name='mutation_type',
            field=models.CharField(max_length=15, choices=[(b'MS', b'Missense'), (b'NS', b'Nonsense'), (b'FSI', b'Frame-Shift Insertion'), (b'IFD', b'In-Frame Deletion'), (b'FSD', b'Frame-Shift Deletion'), (b'IFI', b'In-Frame Insertion')]),
        ),
    ]
