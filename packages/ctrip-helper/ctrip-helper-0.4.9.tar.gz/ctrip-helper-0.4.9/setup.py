# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     setup.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/26
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from setuptools import setup, find_packages

setup(
    name='ctrip-helper',
    version='0.4.9',
    description='This is my ctrip help package',
    long_description='This is my ctrip help package',
    author='ckf10000',
    author_email='ckf10000@sina.com',
    url='https://github.com/ckf10000/ctrip-helper',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'selenium>=4.21.0',
        'pypinyin>=0.51.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
