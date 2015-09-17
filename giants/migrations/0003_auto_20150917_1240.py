# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giants', '0002_auto_20150904_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='display_date',
        ),
        migrations.AddField(
            model_name='person',
            name='display_day',
            field=models.IntegerField(db_index=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='display_month',
            field=models.IntegerField(db_index=True, null=True, blank=True),
        ),
    ]
