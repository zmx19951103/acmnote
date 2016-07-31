# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 02:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(max_length=32)),
                ('permission', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField(max_length=30000, verbose_name='记录')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='problem.MyUser')),
            ],
        ),
        migrations.AlterModelOptions(
            name='problem',
            options={'ordering': ['oj', 'oj_id']},
        ),
        migrations.AlterField(
            model_name='problem',
            name='AC_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='AC时间'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.IntegerField(blank=True, null=True, verbose_name='难度'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='last_update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='最后更新时间'),
        ),
        migrations.AddField(
            model_name='note',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem'),
        ),
    ]
