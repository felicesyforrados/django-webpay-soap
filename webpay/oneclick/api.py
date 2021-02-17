import logging
from datetime import datetime

from .communication import WebpayOneClickWS
from .models import WebpayOneClickPayment, WebpayOneClickMultipleInscription
from .signals import webpay_oneclick_remove_inscription_ok

logger = logging.getLogger(__name__)


class WebpayOneClickInitInscription():
    """
    Clase que ayudara a convertir los valores retornados en initTransaction
    a un objeto
    """
    def __init__(self, token, url, model):
        self.token = token
        self.url = url
        self.model = model


class WebpayOneClickAPI():
    """
    Clase que ayuda a poner interactuar con el WS
    """
    @staticmethod
    def initInscription(username, email, response_url):
        """
        Inicar una conversacion con la capa Interna de interaccion del WS
        @Sent values:
            username
            email
            response_url
        @Return values:
            Object [token, url]
        """
        wo = WebpayOneClickWS().initInscription(username, email, response_url)
        token = wo['token']
        inscription = WebpayOneClickMultipleInscription.objects.create(user=username, token=token)

        return WebpayOneClickInitInscription(
            token=token, url=wo['urlWebpay'], model=inscription)

    @staticmethod
    def authorizePayment(buy_order, tbk_user, username, amount, custom):
        """
        Iniciar comunicacion con la capa de autorizacion de pagos y guardaremos
        registro de la transaccion.
        @Sent values:
            buy_order
            tbk_user
            username
            amount
        @Return vakues:
            Object [
                authorization_code,
                credit_card_type,
                last4_card_digits,
                transaction_id,
                response_code]
        """
        # Obtenemos el usuario, debe estar inscrito con una tarjeta
        woi = None
        try:
            woi = WebpayOneClickMultipleInscription.objects.get(
                user=username, inscrito=True)
        except WebpayOneClickMultipleInscription.DoesNotExist:
            raise Exception('Usuario no encontrado inscrito {}.'.format(username))
        except WebpayOneClickMultipleInscription.MultipleObjectsReturned:
            raise Exception('Posee varias tarjetas activas {}.'.format(username))

        # Guardamos la info del pago que se inicia
        wop = WebpayOneClickPayment.objects.create(
            multipleinscription=woi, buy_order=buy_order, amount=amount)

        # Se inicia la comunicacion con Transbank.
        wo = WebpayOneClickWS().authorizePayment(
            buy_order, tbk_user, username, amount)

        logger.debug("Webpay Oneclick. Respuesta de autorizacion de pago para usuario {}, respuesta {}".format(username, wo))
        logger.debug("order {}".format(buy_order))
        logger.debug("order2 {}".format(wop.buy_order))

        wop.authorization_code = wo['authorizationCode'] if "authorizationCode" in wo else ""
        wop.credit_card_type = wo['creditCardType'] if "creditCardType" in wo else ""
        wop.last4_card_digits = wo['last4CardDigits'] if "last4CardDigits" in wo else ""
        wop.transaction_id = wo['transactionId'] if "transactionId" in wo else ""
        wop.response_code = wo['responseCode'] if "responseCode" in wo else ""
        wop.custom = custom
        wop.save()
        wop.send_signals()

        return wop

    @staticmethod
    def removeInscription(tbk_user, username):
        """
        Metodo que ayudara a revisar la inscripcion de una tarjeta y
        la desactivara.
        @Sent values
            tbk_user
            username
        @Return Values
            boolean
        """
        woi = None
        # Obtenemos el usuario inscrito
        try:
            woi = WebpayOneClickMultipleInscription.objects.get(
                user=username, tbk_user=tbk_user, inscrito=True)
        except WebpayOneClickMultipleInscription.DoesNotExist:
            raise Exception('Usuario no encontrado inscrito {}.'.format(username))
        except WebpayOneClickMultipleInscription.MultipleObjectsReturned:
            raise Exception('Posee varias tarjetas activas {}.'.format(username))

        wo = WebpayOneClickWS().removeInscription(woi.tbk_user, woi.user)

        if wo is True:
            # Desactivamos al usuario de nuestra DB
            woi.inscrito = False
            woi.date_uninscription = datetime.today()
            woi.save()
            webpay_oneclick_remove_inscription_ok.send(sender=woi)
        return wo

    @staticmethod
    def reversePayment(buy_order):
        """
        Metodo que podra reversar un pago ya hecho
        """
        try:
            wop = WebpayOneClickPayment.objects.get(buy_order=buy_order)
        except WebpayOneClickPayment.DoesNotExist:
            raise Exception('Orden de compra no existe {} en la reversa de pago'.format(buy_order))

        wo = WebpayOneClickWS().reversePayment(buy_order)

        if wo["reversed"] is True:
            wop.reverse_code = wo["reverseCode"]
            wop.reverse_date = datetime.today()
            wop.save()
            wop.send_signals()
        return wop
