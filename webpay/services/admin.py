from django.contrib import admin
from .models import WebpayServicesCancellationModel


class WebpayServiceCancellationAdmin(admin.ModelAdmin):
    """
    Modelo de administracion de las cancelaciones Webpay
    """
    list_display = (
        "buyOrder", "authorizationCode", "authorizationDate",
        "nullifiedAmount", "payment_type")

admin.site.register(WebpayServicesCancellationModel, WebpayServiceCancellationAdmin)
