# -*- coding: utf-8 -*-
"""
Implementacion de metodos de comunicacion con Webpay.
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


class WebpayNormalWS():
    """
    Clase que ayuda a toda la comunicacion WS Normal que se hace con Transbank.
    """
    @staticmethod
    def initTransaction(amount, buyOrder, sessionId, urlReturn, urlFinal):
        """
        Iniciaremos una conversacion con Webpay.
        @Sent values:
            WSTransactionType: TR_NORMAL_WS
            sessionId: String
            returnURL: anyURI
            finalURLL: anyURI
            transactionDetails:
                amount: Decimal
                buyOrder: String
                commerceCode: String
            wPMDetail: No se usa en WebpayNormal
            commerceId: String
            buyOrder: String
        @Return values:
            token: String
            url: String
        """
        client = WebpayNormalWS.get_client()
        client.options.cache.clear()

        init = client.factory.create('wsInitTransactionInput')
        init.wSTransactionType = client.factory.create('wsTransactionType').TR_NORMAL_WS
        init.commerceId = settings.WEBPAY_COMMERCE_CODE
        init.buyOrder = buyOrder
        init.sessionId = sessionId
        init.returnURL = urlReturn
        init.finalURL = urlFinal

        detail = client.factory.create('wsTransactionDetail')
        detail.amount = amount
        detail.commerceCode = settings.WEBPAY_COMMERCE_CODE
        detail.buyOrder = buyOrder

        init.transactionDetails.append(detail)
        init.wPMDetail = client.factory.create('wpmDetailInput')

        iniTransaction = client.service.initTransaction(init)
        return iniTransaction

    @staticmethod
    def getTransaction(token):
        """
        Obtener el resultado de una transaccion.
        @Sent values:
            tokenInput: String
        @Return values:
            buyOrder: String
            sessionId: String
            cardDetails:
                cardNumber: String
                cardExpiration: String
            accoutingDate: String MMDD
            transactionDate: String MMDDHHmm
            VCI: String [TSY, TSN, TO, ABO, U3]
            urlRedirection: String
            detailsOutput:
                authorizationCode: String
                paymentTypeCode: String [VD, VN, VC, SI, S2, NC]
                responseCode: String [0, -1, -2, -3, -4, -5, -6, -7, -8]
                Amount: Decimal
                sharesNumber: Int (Cantidades de cuotas)
                commerceCode: String
                buyOrder: String
        """
        client = WebpayNormalWS.get_client()
        client.options.cache.clear()
        transactionResultOutput = client.service.getTransactionResult(token)
        return transactionResultOutput

    @staticmethod
    def acknowledgeTransaction(token):
        """
        Metodo que ayuda a informar a Webpay la correcta recepcion del resultado
        Sent values:
            tokenInput
        """
        client = WebpayNormalWS.get_client()
        client.options.cache.clear()
        acknowledge = client.service.acknowledgeTransaction(token)
        return acknowledge

    @staticmethod
    def get_client():
        """
        Obtenemos la informacion de nuestro cliente.
        """
        return Client(
            settings.WEBPAY_WSDL,
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
