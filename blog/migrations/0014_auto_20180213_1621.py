# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-13 22:21
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20180213_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=tinymce.models.HTMLField(blank=True, unique=True, verbose_name='Autor'),
        ),
    ]
