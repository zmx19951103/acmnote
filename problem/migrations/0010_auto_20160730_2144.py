# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 13:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0009_auto_20160730_1958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-update_time']},
        ),
    ]