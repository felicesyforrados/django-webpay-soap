# !/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '2020.01.15'

setup(
    name='django-webpay-soap',
    version=version,
    description='Aplicación Django para integrar WebPay mediante Webservices',
    author='FyF',
    author_email="dev@felicesyforrados.cl",
    url='https://github.com/felicesyforrados/django-webpay-soap',
    license='MIT license',
    platforms=['any'],
    packages=find_packages(),
    classifiers=[
        "Framework :: Django",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    zip_safe=False,
)
