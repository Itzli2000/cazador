# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 03:47
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Imagen en formato png o jpg', null=True, upload_to=blog.models.get_upload_path, verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='Entrada'),
        ),
    ]
