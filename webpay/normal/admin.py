from django.contrib import admin
from .models import WebpayNormal


class WebpayNormalAdmin(admin.ModelAdmin):
    """
    Modelo de administracion de Ordenes de Webpay
    """
    list_display = (
        "id", "buyOrder", "get_status", "amount", "authorizationCode",
        "paymentTypeCode", "transactionDate", "sharesNumber"
    )
    search_fields = ["buyOrder", "transactionDate"]
    list_per_page = 100

    def get_status(self, instance):
        return instance.status
    get_status.short_description = 'Status'

admin.site.register(WebpayNormal, WebpayNormalAdmin)
