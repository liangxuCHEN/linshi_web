# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRateDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet_name', models.CharField(max_length=40)),
                ('num_sheet', models.IntegerField()),
                ('avg_rate', models.FloatField()),
                ('rates', models.CharField(max_length=256)),
                ('detail', models.TextField()),
                ('num_shape', models.CharField(max_length=512)),
                ('sheet_num_shape', models.CharField(max_length=512)),
            ],
        ),
    ]
