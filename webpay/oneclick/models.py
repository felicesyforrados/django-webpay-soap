# -*- coding: utf-8 -*-
from django.db import models

from .conf import RESPONSE_CODES, PAYMENT_RESPONSE_CODES


class WebpayOneClickInscription(models.Model):
    """
    Modelo para guardar informacion de OneClick
    """
    user = models.CharField(
        'Username del usuario del comercio', max_length=100, primary_key=True)
    token = models.CharField(
        'Token proporcionado por Transbank', max_length=300, blank=True)
    tbk_user = models.CharField(
        'Username del usuario en Transbank', max_length=200, blank=True)
    response_code = models.CharField(
        'Código respuesta de la autorizacion', max_length=10, blank=True)
    authorization_code = models.CharField(
        'Código autorización de la transacción', max_length=8, blank=True)
    creditcard_type = models.CharField(
        'Tipo de tarjeta inscrita por el cliente', max_length=10, blank=True)
    card_number = models.CharField(
        'Últimos 4 números de la tarjeta', max_length=4, blank=True)
    inscrito = models.BooleanField('Esta inscrito correctamente', default=False)
    date_inscription = models.DateTimeField(auto_now=True)

    @property
    def humanized_response_code(self):
        """
        Response code humanizado
        """
        return RESPONSE_CODES.get(self.response_code)

    def __unicode__(self):
        return "User: {}".format(self.user)

    class Meta:
        db_table = "webpay_oneclick_inscription"
        verbose_name = "Webpay OneClick Inscription"


class WebpayOneClickPayment(models.Model):
    """
    Modelo para guardar informacion de los pagos autorizados mediante OneClick.
    """
    inscription = models.ForeignKey(WebpayOneClickInscription, blank=False, null=False)
    buy_order = models.CharField(
        'Orden Compra de la tienda', max_length=42, unique=True)
    amount = models.PositiveIntegerField('Monto transacción', default=0)
    authorization_code = models.CharField(
        'Código autorización de la transacción', max_length=8, blank=True)
    credit_card_type = models.CharField(
        'Tipo de tarjeta inscrita por el cliente', max_length=10, blank=True)
    last4_card_digits = models.CharField(
        'Últimos 4 números de la tarjeta', max_length=4, blank=True)
    transaction_id = models.CharField(
        'Transaction ID', max_length=4, blank=True)
    response_code = models.CharField(
        'Código respuesta de la autorizacion', max_length=10, blank=True)

    @property
    def humanized_response_code(self):
        """
        Response code humanizado
        """
        return PAYMENT_RESPONSE_CODES.get(self.response_code)

    class Meta:
        db_table = "webpay_oneclick_payment"
        verbose_name = "Webpay OneClick Payment"
