# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-03-30 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content2', '0002_auto_20170310_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='gestalten.Gestalt'),
        ),
    ]
