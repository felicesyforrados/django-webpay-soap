"""
Signals que envian mensaje a la app Django
"""
from django.dispatch import Signal


webpay_normal_ok = Signal()  # Pago Webpay normal ok