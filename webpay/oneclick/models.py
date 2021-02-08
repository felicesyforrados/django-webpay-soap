# -*- coding: utf-8 -*-
from django.db import models

from .conf import RESPONSE_CODES, PAYMENT_RESPONSE_CODES
from .signals import (
    webpay_oneclick_inscription_ok, webpay_oneclick_payment_ok,
    webpay_oneclick_reverse_payment)


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
    date_uninscription = models.DateTimeField(null=True, default=None)
    custom = models.CharField(max_length=250, blank=True)

    @property
    def humanized_response_code(self):
        """
        Response code humanizado
        """
        return RESPONSE_CODES.get(self.response_code)

    def send_signals(self):
        """
        Enviar signals a la app Django.
        """
        if str(self.response_code) == "0":  # Inscrito correctamente
            webpay_oneclick_inscription_ok.send(sender=self)

    def __unicode__(self):
        return "User: {}".format(self.user)

    class Meta:
        db_table = "webpay_oneclick_inscription"
        verbose_name = "Webpay OneClick Inscription"


class WebpayOneClickMultipleInscription(models.Model):
    """
    Modelo para guardar Multiples Incripciones de OneClick
    """
    user = models.CharField(
        'Username del usuario del comercio', max_length=100, null=False)
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
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_uninscription = models.DateTimeField(null=True, default=None)
    custom = models.CharField(max_length=250, blank=True)

    @property
    def humanized_response_code(self):
        """
        Response code humanizado
        """
        return RESPONSE_CODES.get(self.response_code)

    def send_signals(self):
        """
        Enviar signals a la app Django.
        """
        if str(self.response_code) == "0":  # Inscrito correctamente
            webpay_oneclick_multiple_inscription_ok.send(sender=self)

    def __unicode__(self):
        return "User: {}".format(self.user)

    class Meta:
        db_table = "webpay_oneclick_multiple_inscription"
        verbose_name = "Webpay OneClick Inscription"


class WebpayOneClickPayment(models.Model):
    """
    Modelo para guardar informacion de los pagos autorizados mediante OneClick.
    """
    inscription = models.ForeignKey(WebpayOneClickInscription, null=True, on_delete=models.CASCADE)
    multipleinscription = models.ForeignKey(WebpayOneClickMultipleInscription, null=True, on_delete=models.CASCADE)
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
    reverse_code = models.CharField(
        'Codigo de transaccion reversada', max_length=30, blank=True)
    payment_date = models.DateTimeField(auto_now=True)
    reverse_date = models.DateTimeField(null=True, default=None)
    custom = models.CharField(max_length=250, blank=True)

    @property
    def humanized_response_code(self):
        """
        Response code humanizado
        """
        return PAYMENT_RESPONSE_CODES.get(self.response_code)

    def send_signals(self):
        """
        Enviar signals a la app Django
        """
        # si existe un reverse code se llama el signal corresponiente
        # si no entonces el pago esta ok
        if str(self.reverse_code) != "":
            webpay_oneclick_reverse_payment.send(sender=self)
        else:
            if str(self.response_code) == "0":
                webpay_oneclick_payment_ok.send(sender=self)

    class Meta:
        db_table = "webpay_oneclick_payment"
        verbose_name = "Webpay OneClick Payment"
