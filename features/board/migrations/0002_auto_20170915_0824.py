# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.CharField(help_text='höchstens 70 Zeichen', max_length=70),
        ),
    ]
