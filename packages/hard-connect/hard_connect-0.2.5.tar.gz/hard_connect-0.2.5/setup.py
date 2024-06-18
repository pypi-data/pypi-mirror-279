#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：setup.py
@Author  ：KING
@Date    ：2024/6/11 18:22 
"""
from setuptools import setup, find_packages

setup(
    name='hard_connect',
    version='0.2.5',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
        'pyserial==3.5',
    ],
    author='kingduyin',
    author_email='kingduyin@gmail.com',
    description='Connect hard device, socket or serial',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/mymodule',  # 模块的主页
    classifiers=[
        # 模块分类
    ],
    python_requires='>=3.6',
)
