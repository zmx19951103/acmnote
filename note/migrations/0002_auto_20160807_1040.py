# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-07 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='标签')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'tag',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='classicnote',
            name='tags',
            field=models.ManyToManyField(to='note.NoteTag'),
        ),
    ]