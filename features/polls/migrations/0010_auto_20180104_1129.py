# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 10:29
from __future__ import unicode_literals

from django.db import connection, migrations


def convert_votes(apps, schema_editor):
    Vote = apps.get_model('polls', 'Vote')
    with connection.cursor() as cursor:
        for v in Vote.objects.all():
            cursor.execute('INSERT INTO polls_simplevote VALUES (%s, \'0\')', [v.id])


def adapt_endorsement(apps, schema_editor):
    SimpleVote = apps.get_model('polls', 'SimpleVote')
    for v in SimpleVote.objects.all():
        SimpleVote.objects.filter(id=v.id).update(endorse_new=v.endorse)


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20180104_1045'),
    ]

    operations = [
        migrations.RunPython(convert_votes),
        migrations.RunPython(adapt_endorsement),
    ]
