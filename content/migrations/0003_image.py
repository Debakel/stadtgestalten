# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20151227_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Content')),
            ],
        ),
    ]
