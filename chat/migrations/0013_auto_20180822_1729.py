# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-22 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180215_1505'),
        ('chat', '0012_chatroom_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=256)),
                ('last_message_id', models.IntegerField(default=0)),
                ('logo', models.ImageField(blank=True, upload_to='')),
                ('has_unread', models.BooleanField(default=True)),
                ('link_id', models.IntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='account.UserProfile')),
                ('friend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='account.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='author',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='friend',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='msg',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chat_room',
        ),
        migrations.AddField(
            model_name='message',
            name='link_id',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
        migrations.AddField(
            model_name='message',
            name='dialog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chat.Dialog'),
        ),
    ]
