# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-16 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temperature', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probe',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reading',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
