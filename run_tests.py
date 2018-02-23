
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import django
import os
import sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(
    DEBUG=True,
    WEBPAY_COMMERCE_CODE="000011",
    WEBPAY_WSDL='https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSWebpayService?wsdl',
    WEBPAY_OUR_PRIVATE_KEY='/certs/ourprivatekey.pem',
    WEBPAY_OUR_PUBLIC_CERT='/certs/ourpublicert.pem',
    WEBPAY_URL_FINAL='mitesting.com',
    WEBPAY_CERT='/certs/webpaycert.pem',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='webpay.normal.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'webpay.normal',
    ),
    LOGGER_WEBPAY='logger_webpay',
    USE_TZ=True,
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                # ... some options here ...
            },
        },
    ]
)

try:
    # Django < 1.8
    from django.test.simple import DjangoTestSuiteRunner
except ImportError:
    # Django >= 1.8
    from django.test.runner import DiscoverRunner as DjangoTestSuiteRunner

django.setup()
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['webpay', ])
if failures:
    sys.exit(failures)
