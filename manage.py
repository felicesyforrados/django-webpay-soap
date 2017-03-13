#!/usr/bin/env python

# This manage.py exists for the purpose of creating migrations
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line

settings.configure(
    DATABASES={
        'default':
        {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test.db',}
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'webpay.normal',
    ] + (['south'] if django.VERSION < (1, 7) else []),
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            'TIMEOUT': 0,
            'KEY_PREFIX': 'webpay_tests_',
        }
    },
    MIDDLEWARE_CLASSES=[],
)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
