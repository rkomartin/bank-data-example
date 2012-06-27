import os
from setuptools import setup, find_packages


setup(
    name='bank_data_example',
    packages=find_packages(),
    install_requires=['veritable'],
    package_data={'': ['*.csv']}
    )
