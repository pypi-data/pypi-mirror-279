#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：test.py
@Author  ：KING
@Date    ：2024/6/13 12:51 
"""
import time

from hard_connect.hard_conn import hard_conn as HardConnect


def test_conn():
    import logging
    hard = HardConnect(conn_type='socket', ip='127.0.0.1', port=60000, logging_level=logging.DEBUG)
    hard.start()
    # hard1 = HardConnect(conn_type='socket', ip='192.168.0.100', port=5001, timeout=0.01)
    # hard = HardConnect(conn_type='serial', device='/dev/tty.usbmodem1202', baud_rate=115200)
    # hard1.start()
    hard.send_receive('>vcm upload(on)')
    print('----', hard.send_receive('>vcm force(10)'))
    time.sleep(1)
    print('----', hard.send_receive('>vcm force(10)'))
    # print(hard.send_receive('>vcm force(10)'))
    # hard.send('>vcm force(50)')
    # hard.send_receive('>vcm force(100)')
    # hard.send('>vcm force(0)')
    print(hard)


if __name__ == '__main__':
    test_conn()