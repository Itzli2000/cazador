# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-13 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_excerpt'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(blank=True, max_length=25, unique=True, verbose_name='Autor'),
        ),
    ]
