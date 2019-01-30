from django.contrib import admin
from .models import WebpayOneClickInscription, WebpayOneClickPayment


class WebpayOneClickInscriptionAdmin(admin.ModelAdmin):
    """
    Modelo de administracion de Inscripciones de Admin
    """
    list_display = ("user", "tbk_user", "response_code", "date_inscription")

admin.site.register(WebpayOneClickInscription, WebpayOneClickInscriptionAdmin)


class WebpayOneClickPaymentAdmin(admin.ModelAdmin):
    """
    Modelo para la administracion de Pagos por Oneclick
    """
    list_display = ("user", "buy_order", "amount", "response_code")

admin.site.register(WebpayOneClickPayment, WebpayOneClickInscriptionAdmin)
