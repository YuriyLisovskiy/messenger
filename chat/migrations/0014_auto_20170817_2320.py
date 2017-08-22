# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_auto_20170817_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='name',
            new_name='user_author_id',
        ),
        migrations.RenameField(
            model_name='chatroom',
            old_name='user_1',
            new_name='user_friend_id',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='user_2',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.UserProfile'),
        ),
    ]
