# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-07 02:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_auto_20160807_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classicnote',
            name='tags',
        ),
        migrations.DeleteModel(
            name='NoteTag',
        ),
    ]
