# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0027_auto_20170830_0054'),
        ('music', '0004_auto_20170903_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chat.UserProfile'),
        ),
        migrations.AddField(
            model_name='song',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chat.UserProfile'),
        ),
    ]
