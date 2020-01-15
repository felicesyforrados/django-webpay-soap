Django Webpay Soap
==================

Aplicacion de integracion entre Django y Webpay.

El actual proyecto soporta los productos Webpay Normal y Webpay OneClick.

Instalación
===========

Agregando a requirements.txt y hacer pip install -r requirements.txt
> git+ssh://git@github.com/felicesyforrados/django-webpay-soap.git#egg=django-webpay-soap

Configuración General
=====================

* Variables en settings.py del proyecto Django.

  > Código comercio
  >> WEBPAY_COMMERCE_CODE = '597020000541'

Configurar URLs en el setting.py del comercio.

Configuración Webpay Normal
===========================

* Variables en settings.py del proyecto Django.

  > URL del WebService
  >> WEBPAY_WSDL = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSWebpayService?wsdl'

  > URL Final del carro de compras.
  >> WEBPAY_URL_FINAL = BASE_URL + '/core/pagos/webpay/final/'

  > Nuestra llave privada .pem
  >> WEBPAY_OUR_PRIVATE_KEY = BASE_DIR + '/certs/ourprivatekey.pem'

  > Nuestra certificado público .pem
  >> WEBPAY_OUR_PUBLIC_CERT = BASE_DIR + '/certs/ourpublicert.pem'

  > Certificado de WebPay .pem
  >> WEBPAY_CERT = BASE_DIR + '/certs/webpaycert.pem'

Configuración Webpay OneClick
=============================

  > URL del WebService
  >> WEBPAY_ONECLICK_WSDL = 'https://webpay3gint.transbank.cl/webpayserver/wswebpay/OneClickPaymentService?wsdl'

  > URL Final del carro de compras.
  >> WEBPAY_ONECLICK_URL_FINAL = BASE_URL + '/core/pagos/webpay/final/'

  > Nuestra llave privada .pem
  >> WEBPAY_ONECLICK_OUR_PRIVATE_KEY = BASE_DIR + '/certs/ourprivatekey.pem'

  > Nuestra certificado público .pem
  >> WEBPAY_ONECLICK_OUR_PUBLIC_CERT = BASE_DIR + '/certs/ourpublicert.pem'

  > Certificado de WebPay .pem
  >> WEBPAY_ONECLICK_CERT = BASE_DIR + '/certs/webpaycert.pem'


Configuración Webpay Anulación
=============================
  > URL del WebService
  >> WEBPAY_SERVICES_WSDL = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSCommerceIntegrationService?wsdl'
