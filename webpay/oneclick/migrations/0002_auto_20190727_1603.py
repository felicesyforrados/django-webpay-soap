# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-27 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oneclick', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpayoneclickinscription',
            name='date_uninscription',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='webpayoneclickpayment',
            name='reverse_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='webpayoneclickpayment',
            name='reverse_code',
            field=models.CharField(blank=True, max_length=30, verbose_name=b'Codigo de transaccion reversada'),
        ),
    ]
