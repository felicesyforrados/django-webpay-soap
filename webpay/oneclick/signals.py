"""
Signals que envian mensajes a la app Django
"""
from django.dispatch import Signal


webpay_oneclick_inscription_ok = Signal()

webpay_oneclick_multiple_inscription_ok = Signal()

webpay_oneclick_payment_ok = Signal()

webpay_oneclick_remove_inscription_ok = Signal()

webpay_oneclick_reverse_payment = Signal()
