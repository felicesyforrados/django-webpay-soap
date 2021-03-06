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


class WebpayOneClickWS():
    """
    Clase que ayuda a toda la comunicacion WS OneClick que se hace con
    Transbank.
    """
    @staticmethod
    def initInscription(username, email, response_url):
        """
        Iniciaremos una conversacion con Webapy
        @Sent values:
            username
            email
            response_url
        @Return values:
            token: String
            url: String
        """
        client = WebpayOneClickWS.get_client()
        client.options.cache.clear()

        inscription_input = client.factory.create('oneClickInscriptionInput')
        inscription_input.username = username
        inscription_input.email = email
        inscription_input.responseURL = response_url

        init_inscription = client.service.initInscription(inscription_input)
        return init_inscription

    @staticmethod
    def finishInscription(token):
        """
        Verificaremos el estado de la inscripcion con Webpay.
        @Sent values:
            token
        @Return Values
            estado
            tbkUser
        """
        client = WebpayOneClickWS.get_client()
        client.options.cache.clear()

        finish_input = client.factory.create('oneClickFinishInscriptionInput')
        finish_input.token = token

        finish_inscription = client.service.finishInscription(finish_input)
        return finish_inscription

    @staticmethod
    def authorizePayment(buy_order, tbk_user, username, amount):
        """
        Realizamos un pago al usuario correspondiente
        @Sent values:
            buy_order
            tbk_user
            username
            amount
        @Return Values
            authorizationCode
            creditCardType
            last4CardDigits
            transactionId
            responseCode
        """
        client = WebpayOneClickWS.get_client()
        client.options.cache.clear()

        authorize_input = client.factory.create('oneClickPayInput')
        authorize_input.buyOrder = buy_order
        authorize_input.tbkUser = tbk_user
        authorize_input.username = username
        authorize_input.amount = amount

        authorize_payment = client.service.authorize(authorize_input)
        return authorize_payment

    @staticmethod
    def removeInscription(tbk_user, username):
        """
        Metodo que nos ayudara a poder eliminar la inscripcion del cliente.
        @Sent values:
            tbk_user
            username
        @Return values
            boolean
        """
        client = WebpayOneClickWS.get_client()
        client.options.cache.clear()
        remove_inscription = client.factory.create('oneClickRemoveUserInput')
        remove_inscription.tbkUser = tbk_user
        remove_inscription.username = username
        return client.service.removeUser(remove_inscription)

    @staticmethod
    def reversePayment(buy_order):
        """
        Metodo que nos ayudara a poder reversar un pago hecho con OneClick
        """
        client = WebpayOneClickWS.get_client()
        client.options.cache.clear()
        reverse_payment = client.factory.create('oneClickReverseInput')
        reverse_payment.buyorder = buy_order
        return client.service.codeReverseOneClick(reverse_payment)

    @staticmethod
    def get_client():
        """
        Obtenemos la informacion de nuestro cliente.
        """
        return Client(
            settings.WEBPAY_ONECLICK_WSDL,
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
