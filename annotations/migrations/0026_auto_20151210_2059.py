# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0025_reference_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gene',
            old_name='locus_end',
            new_name='end_pos',
        ),
        migrations.RenameField(
            model_name='gene',
            old_name='locus_begin',
            new_name='start_pos',
        ),
    ]
