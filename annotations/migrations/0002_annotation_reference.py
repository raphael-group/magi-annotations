# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='reference',
            field=models.ForeignKey(default='', to='annotations.Reference'),
            preserve_default=False,
        ),
    ]
