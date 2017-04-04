# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from .conf import STATUS_CODES
from .signals import webpay_normal_ok


class WebpayNormal(models.Model):
    """
    Modelo para guardar toda la data informada por Webpay.
    """
    buyOrder = models.CharField(
        'Orden Compra de la tienda', max_length=42, unique=True)
    sessionId = models.CharField(
        'Identificador de sesión', max_length=80, blank=True)
    cardNumber = models.CharField(
        'Últimos 4 números de la tarjeta', max_length=4, blank=True)
    accountingDate = models.CharField(
        'Fecha de la autorización', blank=True, null=True, max_length=20)
    transactionDate = models.CharField(
        'Fecha y hora de la autorización', blank=True, null=True, max_length=100)
    authorizationCode = models.CharField(
        'Código autorización de la transacción', max_length=8, blank=True)
    paymentTypeCode = models.CharField(
        'Tipo de pago de la transacción', max_length=10, blank=True)
    responseCode = models.CharField(
        'Código respuesta de la autorizacion', max_length=10, blank=True)
    amount = models.PositiveIntegerField('Monto transacción', default=0)
    sharesNumber = models.CharField(
        'Cantidad de cuotas', max_length=10, blank=True)
    commerceCode = models.CharField(
        'Código del comercio', max_length=80, blank=True)
    token = models.CharField(
        'Token', max_length=100, blank=True)
    custom = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'webpay_normal'
        verbose_name = "Orden de compra WebPay"

    def send_signals(self):
        """
        Enviar un Signal para la app Django
        """
        if self.responseCode == 0:  # Pagado
            webpay_normal_ok.send(sender=self)

    @property
    def status(self):
        """
        Estatus humanizado
        """
        return STATUS_CODES.get(responseCode)

    def __unicode__(self):
        if self.paymentTypeCode == 'VN' or self.paymentTypeCode == 'VD':
            return "<Webpay Normal Contado: {}>".format(self.buyOrder)
        else:
            return "<Webpay Normal Cuotas: {}>".format(self.buyOrder)
