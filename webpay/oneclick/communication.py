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
                    keyfile=settings.WEBPAY_OUR_PRIVATE_KEY,
                    certfile=settings.WEBPAY_OUR_PUBLIC_CERT,
                    their_certfile=settings.WEBPAY_CERT,
                ),
            ],
        )
