# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0007_auto_20170224_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorship',
            options={'ordering': ('time_created',)},
        ),
    ]