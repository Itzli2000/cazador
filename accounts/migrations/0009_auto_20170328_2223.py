# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_billingaddress_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono'),
        ),
    ]
