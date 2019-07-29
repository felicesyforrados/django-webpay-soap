from django.conf import settings

from .communication import WebpayServices
from .models import WebpayServicesCancellationModel


class WebpayServicesAPI():
    """
    Clase que ayudara a interactuar con los servicios extra que tiene Webpay
    """

    @staticmethod
    def cancelTransaction(
            authorizationCode, authorizedAmount, buyOrder, nullifyAmount,
            payment_type):
        """
        Iniciar conversacion con el WS correspondiente para anular una
        transaccion
        @Sent values:
            authorizationCode
            authorizedAmount
            buyOrder
            nullifyAmount
        @Return Values:
            Model Object
        """
        if payment_type == "NORMAL":
            commerceId = settings.WEBPAY_COMMERCE_CODE
        elif payment_type == "ONECLICK":
            commerceId = settings.WEBPAY_ONECLICK_COMMERCE_CODE
        w = WebpayServices().nullifyTransaction(
            authorizationCode=authorizationCode,
            authorizedAmount=authorizedAmount,
            buyOrder=buyOrder,
            commerceId=commerceId,
            nullifyAmount=nullifyAmount,
            payment_type=payment_type)
        # Creamos la tupla en el modelo
        model = WebpayServicesCancellationModel(
            token=w["token"],
            buyOrder=buyOrder,
            authorizationCode=w["authorizationCode"],
            authorizationDate=w["authorizationDate"],
            balance=w["balance"],
            nullifiedAmount=w["nullifiedAmount"],
            commerceCode=commerceId,
            payment_type=payment_type
        )
        model.send_signals()
        model.save()
        return model
