from .communication import WebpayOneClickWS
from .models import WebpayOneClickInscription, WebpayOneClickPayment


class WebpayOneClickInitInscription():
    """
    Clase que ayudara a convertir los valores retornados en initTransaction
    a un objeto
    """
    def __init__(self, token, url):
        self.token = token
        self.url = url

class WebpayOneClickAuthorization():
    """
    Clase que ayudara a normalizar los valores retornados por authorizePayment
    """
    def __init__(
        self, buy_order, tbk_user, username, amount, authorization_code,
        credit_card_type, last4_card_digits, transaction_id, response_code):
        self.buy_order = buy_order
        self.tbk_user = tbk_user
        self.username = username
        self.amount = amount
        self.authorization_code = authorization_code
        self.credit_card_type = credit_card_type
        self.last4_card_digits = last4_card_digits
        self.transaction_id = transaction_id
        self.response_code = response_code


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
        model, created = WebpayOneClickInscription.objects.get_or_create(user=username)
        if not created and model.inscrito is True:
            raise Exception('User is subscribed')
        wo = WebpayOneClickWS().initInscription(username, email, response_url)
        token = wo['token']
        model.token = token
        model.save()
        return WebpayOneClickInitInscription(token=token, url=wo['urlWebpay'])

    @staticmethod
    def authorizePayment(buy_order, tbk_user, username, amount):
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
            woi = WebpayOneClickInscription.objects.get(
                user=username, inscrito=True)
        except WebpayOneClickInscription.DoesNotExist:
            raise Exception('Usuario no encontrado inscrito.')

        # Guardamos la info del pago que se inicia
        wop = WebpayOneClickPayment.objects.create(
            user=woi.user, buy_order=buy_order, amount=amount)

        # Se inicia la comunicacion con Transbank.
        wo = WebpayOneClickWS().authorizePayment(
            buy_order, tbk_user, username, amount)
        return WebpayOneClickAuthorization(
            buy_order=buy_order,
            tbk_user=tbk_user,
            username=username,
            amount=amount,
            authorization_code=wo['authorization_code'],
            credit_card_type=wo['credit_card_type'],
            last4_card_digits=wo['last4_card_digits'],
            transaction_id=wo['transaction_id'],
            response_code=wo['response_code'])
