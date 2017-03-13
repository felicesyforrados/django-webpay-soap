try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

from .views import webpay_normal_verificacion, webpay_normal_termina

urlpatterns = [
    url(r'^normal/verificacion/$', webpay_normal_verificacion, name="webpay_normal_verificacion"),
    url(r'^normal/termina/$', webpay_normal_termina, name="webpay_normal_termina"),
]