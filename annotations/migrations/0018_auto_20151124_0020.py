# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotations', '0017_auto_20151123_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interaction',
            name='user',
        ),
        migrations.AddField(
            model_name='interactionreference',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='interactionreference',
            unique_together=set([('identifier', 'interaction')]),
        ),
    ]
