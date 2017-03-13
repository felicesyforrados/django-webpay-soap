Django Webpay Soap
==================

Aplicacion de integracion entre Django y Webpay.


Instalación
===========

Agregando a requirements.txt y hacer pip install -r requirements.txt
> git+ssh://git@github.com/felicesyforrados/django-webpay-soap.git#egg=django-webpay-soap

Configuración
==============

* Variables en settings.py del proyecto Django.

  > Código comercio
  >> WEBPAY_COMMERCE_CODE = '597020000541'

  > URL del WebService
  >> WEBPAY_WSDL = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSWebpayService?wsdl'
  
  > Nuestra llave privada .pem
  >> WEBPAY_OUR_PRIVATE_KEY = BASE_DIR + '/certs/ourprivatekey.pem'
  
  > Nuestra certificado público .pem
  >> WEBPAY_OUR_PUBLIC_CERT = BASE_DIR + '/certs/ourpublicert.pem'
  
  > Certificado de WebPay .pem
  >> WEBPAY_CERT = BASE_DIR + '/certs/webpaycert.pem'
