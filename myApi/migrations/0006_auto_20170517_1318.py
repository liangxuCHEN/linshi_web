# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 05:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApi', '0005_productratedetail_same_bin_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productratedetail',
            old_name='doc_url',
            new_name='empty_sections',
        ),
    ]
