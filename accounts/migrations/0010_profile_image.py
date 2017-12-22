# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-10 02:39
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170328_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, help_text='Imagen en formato png o jpg', null=True, upload_to=accounts.models.get_upload_path, verbose_name='Imagen'),
        ),
    ]
