# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_remove_userprofile_user_background_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_background_photo',
            field=models.ImageField(default='1.jpg', upload_to=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_logo',
            field=models.ImageField(default='1.jpg', upload_to=''),
        ),
    ]
