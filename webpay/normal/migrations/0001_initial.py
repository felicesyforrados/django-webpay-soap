# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebpayNormal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyOrder', models.CharField(unique=True, max_length=42, verbose_name=b'Orden Compra de la tienda')),
                ('sessionId', models.CharField(max_length=80, verbose_name=b'Identificador de sesi\xc3\xb3n', blank=True)),
                ('cardNumber', models.CharField(max_length=4, verbose_name=b'\xc3\x9altimos 4 n\xc3\xbameros de la tarjeta', blank=True)),
                ('accountingDate', models.CharField(max_length=20, null=True, verbose_name=b'Fecha de la autorizaci\xc3\xb3n', blank=True)),
                ('transactionDate', models.CharField(max_length=100, null=True, verbose_name=b'Fecha y hora de la autorizaci\xc3\xb3n', blank=True)),
                ('authorizationCode', models.CharField(max_length=8, verbose_name=b'C\xc3\xb3digo autorizaci\xc3\xb3n de la transacci\xc3\xb3n', blank=True)),
                ('paymentTypeCode', models.CharField(max_length=10, verbose_name=b'Tipo de pago de la transacci\xc3\xb3n', blank=True)),
                ('responseCode', models.CharField(max_length=10, verbose_name=b'C\xc3\xb3digo respuesta de la autorizacion', blank=True)),
                ('amount', models.PositiveIntegerField(default=0, verbose_name=b'Monto transacci\xc3\xb3n')),
                ('sharesNumber', models.CharField(max_length=10, verbose_name=b'Cantidad de cuotas', blank=True)),
                ('commerceCode', models.CharField(max_length=80, verbose_name=b'C\xc3\xb3digo del comercio', blank=True)),
                ('token', models.CharField(max_length=100, verbose_name=b'Token', blank=True)),
                ('custom', models.CharField(max_length=250, blank=True)),
            ],
            options={
                'db_table': 'webpay_normal',
                'verbose_name': 'Orden de compra WebPay',
            },
        ),
    ]
