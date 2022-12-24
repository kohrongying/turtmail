# -*- coding: utf-8 -*-

from setuptools import setup


def required_packages():
    with open('requirements.txt') as f:
        return [line.strip() for line in f.readlines()]


setup(
    name='payslip_mailer',
    version='1.0',
    packages=["payslip_mailer"],
    entry_points={
        'console_scripts': [
            'payslip_mailer = payslip_mailer.payslip_mailer:main',
        ],
    },
    install_requires=required_packages()
)
