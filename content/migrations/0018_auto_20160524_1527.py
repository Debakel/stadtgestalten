# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 13:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_auto_20160506_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='content.Content'),
        ),
    ]
