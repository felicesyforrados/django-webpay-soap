# -*- coding: utf-8 -*-
"""
Implementacion de servicios extra de Webpay
"""
import logging

from django.conf import settings
from suds.client import Client
from suds.transport.https import HttpTransport
from suds.wsse import Security
from wsse.suds import WssePlugin

logging.basicConfig()
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)


class WebpayServices():

    @staticmethod
    def nullifyTransaction(
            authorizationCode, authorizedAmount, buyOrder, commerceId,
            nullifyAmount, payment_type="NORMAL"):
        """
        Metodo que ayuda a anular una venta hecha en Webpay.
        @Sent values:
            authorizationCode
            authorizedAmount
            buyOrder
            commerceId
            nullifyAmount
        @Return Values:
            Token
            authorizationCode
            authorizationDate
            Balance
            nullifiedAmount
        """
        # Identificamos si es anulacion Webpay normal o Oneclick
        if payment_type == "NORMAL":
            client = WebpayServices.get_normal_client()
            client.options.cache.clear()
        elif payment_type == "ONECLICK":
            client = WebpayServices.get_oneclick_client()
            client.options.cache.clear()
        nullification_input = client.factory.create('nullificationInput')
        nullification_input.authorizationCode = authorizationCode
        nullification_input.authorizedAmount = authorizedAmount
        nullification_input.buyOrder = buyOrder
        nullification_input.commerceId = commerceId
        nullification_input.nullifyAmount = nullifyAmount
        nullify = client.service.nullify(nullification_input)
        return nullify

    @staticmethod
    def get_normal_client():
        """
        Obtenemos la informacion de nuestro cliente Normal.
        """
        return Client(
            settings.WEBPAY_SERVICES_WSDL,
            transport=HttpTransport(),
            wsse=Security(),
            plugins=[
                WssePlugin(
                    keyfile=settings.WEBPAY_OUR_PRIVATE_KEY,
                    certfile=settings.WEBPAY_OUR_PUBLIC_CERT,
                    their_certfile=settings.WEBPAY_CERT,
                ),
            ],
        )

    @staticmethod
    def get_oneclick_client():
        """
        Obtenemos la informacion de nuestro cliente Oneclick.
        """
        return Client(
            settings.WEBPAY_SERVICES_WSDL,
            transport=HttpTransport(),
            wsse=Security(),
            plugins=[
                WssePlugin(
                    keyfile=settings.WEBPAY_ONECLICK_OUR_PRIVATE_KEY,
                    certfile=settings.WEBPAY_ONECLICK_OUR_PUBLIC_CERT,
                    their_certfile=settings.WEBPAY_ONECLICK_CERT,
                ),
            ],
        )
