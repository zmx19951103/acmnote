# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-07 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0005_notetag'),
    ]

    operations = [
        migrations.AddField(
            model_name='classicnote',
            name='tags',
            field=models.ManyToManyField(to='note.NoteTag'),
        ),
    ]
