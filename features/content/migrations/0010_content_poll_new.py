# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-22 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20180222_1033'),
        ('content2', '0009_auto_20180109_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='poll_new',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_new', to='polls.WorkaroundPoll'),
        ),
    ]
