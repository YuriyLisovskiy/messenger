# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 20:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_userprofile_chat_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='chat_room',
        ),
    ]