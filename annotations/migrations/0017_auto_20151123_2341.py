# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotations', '0016_auto_20151120_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='interaction',
            unique_together=set([('source', 'target', 'input_source')]),
        ),
    ]
