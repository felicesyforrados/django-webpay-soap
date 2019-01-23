import logging
import traceback

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .communication import WebpayOneClickWS

logger = logging.getLogger(__name__)


@csrf_exempt
def webpay_oneclick_finish(request):
    """
    Vista que sera consultara por metodo POST por Transbank para entregarnos
    el token del estado de la inscripcion de Webpay OneClick.
    """
    token = request.POST.get("TBK_TOKEN")
    urlRedirection = settings.WEBPAY_ONECLICK_URL_FINAL
    logger.debug("Webpay OneClick. Data recibida por Transbank {}".format(
        request.POST))
    if token:
        try:
            get_finish_inscription = WebpayOneClickWS().finishInscription(token)
            logger.debug('Webpay OneClick. Token {} Respuesta {}'.format(
                token, get_finish_inscription))
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
