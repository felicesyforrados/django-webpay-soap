try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

from .views import webpay_oneclick_finish

urlpatterns = [
    url(r'^finish/$', webpay_oneclick_finish, name="webpay_oneclick_finish"),
]
