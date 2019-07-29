# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from .conf import PAYMENT_TYPES
from .signals import webpay_payment_cancellation


class WebpayServicesCancellationModel(models.Model):
    """
    Modelo que ayudara a guardar las cancelaciones.
    """
    token = models.CharField(
        'Token', max_length=100, blank=True)
    buyOrder = models.CharField(
        'Orden Compra de la tienda', max_length=42, unique=True)
    authorizationCode = models.CharField(
        'Código autorización de la transacción', max_length=8, blank=True)
    authorizationDate = models.CharField(
        'Fecha y hora de la autorización', blank=True, null=True, max_length=100)
    balance = models.CharField(
        'Balance', max_length=20, blank=True, null=True,)
    nullifiedAmount = models.CharField(
        'Monto anulado', max_length=15, blank=True, null=True)
    payment_type = models.CharField(
        "Tipo de pago anulado", max_length=15, choices=PAYMENT_TYPES, null=True, blank=True)
    commerceCode = models.CharField(
        'Código del comercio', max_length=80, blank=True)
    date_cancellation = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "webpay_services_cancellation"
        verbose_name = "Cancelacion de ordenes de compra Webpay"

    def send_signals(self):
        """
        Enviar un signal para la app Django
        """
        if self.authorizationCode:
            webpay_payment_cancellation.send(sender=self)

    def __unicode__(self):
        return "<Webpay {} Cancelacion: {}>".format(self.payment_type, self.buyOrder)
