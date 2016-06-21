# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0020_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='interactionreference',
            name='db',
            field=models.CharField(default='PMID', max_length=30, choices=[(b'PMID', b'PubMed'), (b'PMC', b'PubMed Central')]),
            preserve_default=False,
        ),
    ]
