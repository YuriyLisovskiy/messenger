# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-28 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20180125_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='logo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]