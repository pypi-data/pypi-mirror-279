# setup.py
from setuptools import setup, find_packages

setup(
    name='dedllogin',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)