from django.contrib import admin
from .models import WebpayOneClickInscription


class WebpayOneClickInscriptionAdmin(admin.ModelAdmin):
    """
    Modelo de administracion de Inscripciones de Admin
    """
    list_display = ("user", "tbk_user", "response_code", "date_inscription")

admin.site.register(WebpayOneClickInscription, WebpayOneClickInscriptionAdmin)
