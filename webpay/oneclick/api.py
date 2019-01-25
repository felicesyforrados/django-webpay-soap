from .communication import WebpayOneClickWS


class WebpayOneClickInitInscription():
    """
    Clase que ayudara a convertir los valores retornados en initTransaction
    a un objeto
    """
    def __init__(self, token, url):
        self.token = token
        self.url = url


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
        return WebpayOneClickInitInscription(
            token=wo['token'], url=wo['urlWebpay'])
