# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('associations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='association',
            name='slug',
            field=models.SlugField(default=None, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='association',
            unique_together=set([('entity_id', 'entity_type', 'slug')]),
        ),
    ]
