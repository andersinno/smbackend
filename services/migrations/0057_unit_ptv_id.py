# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-08 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0056_add_service_ext_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='ptv_id',
            field=models.UUIDField(db_index=True, null=True, unique=True),
        ),
    ]
