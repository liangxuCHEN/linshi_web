# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 02:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApi', '0004_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='productratedetail',
            name='same_bin_list',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
