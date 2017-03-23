# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0008_text_in_reply_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replykey',
            name='gestalt',
        ),
        migrations.RemoveField(
            model_name='replykey',
            name='text',
        ),
        migrations.RemoveField(
            model_name='text',
            name='author',
        ),
        migrations.RemoveField(
            model_name='text',
            name='container_type',
        ),
        migrations.RemoveField(
            model_name='text',
            name='in_reply_to',
        ),
        migrations.DeleteModel(
            name='ReplyKey',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
    ]