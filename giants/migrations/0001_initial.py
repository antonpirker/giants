# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'person_images', blank=True)),
                ('wikipedia_link', models.CharField(max_length=1000, null=True, blank=True)),
                ('additional_link', models.CharField(max_length=1000, null=True, blank=True)),
                ('date_shown', models.DateField(null=True, blank=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
            ],
        ),
    ]
