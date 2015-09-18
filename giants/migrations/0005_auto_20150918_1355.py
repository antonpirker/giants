# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giants', '0004_auto_20150918_1305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='is_image_is_from_wikipedia',
            new_name='is_image_from_wikipedia',
        ),
    ]
