# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20180215_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='has_unread',
            field=models.BooleanField(default=True),
        ),
    ]