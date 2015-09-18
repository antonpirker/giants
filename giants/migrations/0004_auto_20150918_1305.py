# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giants', '0003_auto_20150917_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='display_day',
            new_name='display_order',
        ),
        migrations.RemoveField(
            model_name='person',
            name='display_month',
        ),
        migrations.AddField(
            model_name='person',
            name='image_attribution',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='is_image_is_from_wikipedia',
            field=models.BooleanField(default=False),
        ),
    ]
