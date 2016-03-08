# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-07 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0017_auto_20160215_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='entities.Membership', to='entities.Gestalt'),
        ),
    ]
