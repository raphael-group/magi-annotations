# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0009_auto_20150922_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='last_edited',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 47, 51, 505193, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
