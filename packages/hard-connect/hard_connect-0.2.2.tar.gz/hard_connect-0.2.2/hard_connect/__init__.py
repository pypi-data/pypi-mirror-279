#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：__init__.py
@Author  ：KING
@Date    ：2024/6/11 18:08 
"""
from hard_connect.hard_conn import hard_conn as HardConnect
from hard_connect.hard_conn import HardConnSock, HardConnSerial

__all__ = ['HardConnect']
