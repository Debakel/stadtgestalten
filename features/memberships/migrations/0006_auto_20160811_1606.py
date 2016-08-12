# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0005_auto_20160811_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships_created', to='entities.Gestalt'),
        ),
    ]
