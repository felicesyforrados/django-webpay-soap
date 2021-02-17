from django.contrib import admin
from .models import WebpayOneClickMultipleInscription, WebpayOneClickPayment


class WebpayOneClickMultipleInscriptionAdmin(admin.ModelAdmin):
    """
    Modelo de administracion de Inscripciones de Admin
    """
    list_display = ("user", "tbk_user", "response_code", "date_inscription")

admin.site.register(WebpayOneClickMultipleInscription, WebpayOneClickMultipleInscriptionAdmin)


class WebpayOneClickPaymentAdmin(admin.ModelAdmin):
    """
    Modelo para la administracion de Pagos por Oneclick
    """
    list_display = ("inscription", "buy_order", "amount", "response_code")

admin.site.register(WebpayOneClickPayment, WebpayOneClickMultipleInscriptionAdmin)
