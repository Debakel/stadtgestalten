# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-22 09:34
from __future__ import unicode_literals

from django.db import migrations


def move_polls_to_workaround(apps, schema_editor):
    Poll = apps.get_model('polls', 'Poll')
    WorkaroundPoll = apps.get_model('polls', 'WorkaroundPoll')

    for poll in Poll.objects.all():
        wp = WorkaroundPoll.objects.create()
        poll.poll_new = wp
        poll.save()
        for option in poll.options.all():
            option.poll_new = wp
            option.save()


class Migration(migrations.Migration):

    dependencies = [
        ('content2', '0010_content_poll_new'),
        ('polls', '0014_auto_20180222_1033'),
    ]

    operations = [
        migrations.RunPython(move_polls_to_workaround)
    ]
