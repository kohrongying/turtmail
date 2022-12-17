from setuptools import setup, find_packages


def required_packages():
    with open('requirements.txt') as f:
        return [line.strip() for line in f.readlines()]


setup(
    name='payslip_mailer',
    version='1.0',
    packages=find_packages(),  # include/exclude arguments take * as wildcard, . for any sub-package names
    scripts=["bin/payslip-mailer"],
    install_requires=required_packages()
)
