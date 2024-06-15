# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:29:28 2024

@author: DAlexander, imported from GPT
"""

from setuptools import setup, find_packages

setup(
    name='pyOrcas',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'pymodbus[serial]'
    ],
    include_package_data=True,
    description='A Python package for communicating with the Orca motor using Modbus.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daniel Alexander',
    author_email='dralexander@irisdynamics.com',
    url='https://github.com/dralexan/pyOrcas',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)