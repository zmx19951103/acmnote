# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20160803_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='var',
        ),
        migrations.AlterField(
            model_name='problem',
            name='last_update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='最后更新时间'),
        ),
    ]
