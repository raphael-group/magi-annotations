# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotations', '0018_auto_20151124_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteractionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_positive', models.BooleanField()),
                ('reference', models.ForeignKey(to='annotations.InteractionReference')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='interactionvote',
            unique_together=set([('user', 'reference')]),
        ),
    ]
