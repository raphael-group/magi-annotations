# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0010_annotation_last_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 30, 854527, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cancer',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 34, 26909, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cancer',
            name='last_edited',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 36, 783337, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mutation',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 40, 428265, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mutation',
            name='last_edited',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 43, 184416, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reference',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 46, 109470, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reference',
            name='last_edited',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 19, 49, 48, 854568, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
