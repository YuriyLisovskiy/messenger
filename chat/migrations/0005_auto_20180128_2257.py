# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-28 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20180128_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='author_logo',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]