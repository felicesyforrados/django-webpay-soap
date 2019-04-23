import logging
import traceback

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt

from .communication import WebpayOneClickWS
from .models import WebpayOneClickInscription

logger = logging.getLogger(__name__)


def webpay_oneclick_model(token, get_finish_inscription):
    """
    Metodo que ayudara a guardar el modelo.
    """
    oneclick_model = WebpayOneClickInscription.objects.get(token=token)
    oneclick_model.response_code = get_finish_inscription['responseCode']
    if str(oneclick_model.response_code) == '0':
        oneclick_model.inscrito = True
        oneclick_model.tbk_user = get_finish_inscription['tbkUser']
        oneclick_model.authorization_code = get_finish_inscription['authCode']
        oneclick_model.card_number = get_finish_inscription['last4CardDigits']
        oneclick_model.creditcard_type = get_finish_inscription['creditCardType']
    oneclick_model.save()
    oneclick_model.send_signals()


@csrf_exempt
def webpay_oneclick_finish(request):
    """
    Vista que sera consultara por metodo POST por Transbank para entregarnos
    el token del estado de la inscripcion de Webpay OneClick.
    """
    token = request.POST.get("TBK_TOKEN")
    urlRedirection = settings.WEBPAY_ONECLICK_URL_FINAL_INSCRIPCION
    logger.debug("Webpay OneClick. Data recibida por Transbank {}".format(
        request.POST))
    if token:
        try:
            get_finish_inscription = WebpayOneClickWS().finishInscription(token)
            logger.debug('Webpay OneClick. Token {} Respuesta {}'.format(
                token, get_finish_inscription))
            webpay_oneclick_model(token, get_finish_inscription)
        except Exception, e:
            logger.error('Webpay OneClick. Ocurrion un error al consultar Token enviado por Transbank {}. Error {} Traza {}'.format(
                token, e, traceback.format_exc()))

        # Haremos un response del Token que nos envia Transbank y haremos un
        # automatico redirect con JS
        template = Template("""
            <body background='https://webpay3g.transbank.cl/webpayserver/imagenes/background.gif'>
                <form action='{{urlRedirection}}' method='post' id='webpay_form'>
                    <input type='hidden' name='token_ws' value='{{token}}'>
                </form>
                <script>document.getElementById('webpay_form').submit();</script>
            </body>
        """)
        context = Context({"urlRedirection": urlRedirection, "token": token})
        return HttpResponse(template.render(context))
    return HttpResponseBadRequest()
