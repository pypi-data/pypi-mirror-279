# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 21:40:03 2024

@author: Subham Divakar
"""

from setuptools import setup, find_packages

setup(
    name='sdcfc',
    version='0.1.1',
    description='SDCFC(Secure Data Certificate Format Converter) This tool converts certs from one format(PEM, DER, PKCS12) files to other formats(PEM, DER, PKCS12).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Subham Divakar',
    author_email='shubham.divakar@gmail.com',
    url='https://github.com/shubham10divakar/sdcfc',
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'pyOpenSSL',
    ],
    entry_points={
        'console_scripts': [
            'sdcfc=sdcfc:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
