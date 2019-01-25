from django.db import models


class WebpayOneClickInscription(models.Model):
    """
    Modelo para guardar informacion de OneClick
    """
    token = models.CharField(
        'Token proporcionado por Transbank', max_length=300, blank=True)
    user = models.CharField(
        'Username del usuario del comercio', max_length=100, blank=True)
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


    class Meta:
        db_table = "webpay_oneclick_inscription"
        verbose_name = "Webpay OneClick Inscription"
