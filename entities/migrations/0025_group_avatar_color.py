# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0024_auto_20160506_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='avatar_color',
            field=models.TextField(default='#a1b726', max_length='7'),
        ),
    ]
