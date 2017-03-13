# -*- coding: utf-8 -*-
from .communication import WebpayNormalWS
from .models import WebpayNormal


class WebpayInitTransaction():
    """
    Clase que ayudara a convertir los valores retornados en initTransaction
    a un objeto
    """
    def __init__(self, token, url, model):
        self.token = token
        self.url = url
        self.model = model


class WebpayNormalAPI():
    """
    Clase que ayudara a poder interactuar con la capa de conexion WebService
    y la app
    """
    @staticmethod
    def initTransaction(amount, buyOrder, sessionId, urlReturn, urlFinal):
        """
        Inicar una conversacion con la capa Interna de interaccion del WS
        @Sent values:
            amount
            buyOrder
            sessinId
            urlReturn
            urlFinal
        @Return values:
            Object [token, url, model]
        """
        wp = WebpayNormalWS().initTransaction(
            amount, buyOrder, sessionId, urlReturn, urlFinal)
        token = wp['token']
        # Creamos una tupla en el modelo
        model = WebpayNormal(
            buyOrder=buyOrder, amount=amount, sessionId=sessionId, token=token)
        model.save()
        return WebpayInitTransaction(
            token=token, url=wp['url'], model=model)
