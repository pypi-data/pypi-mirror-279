#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：test.py
@Author  ：KING
@Date    ：2024/6/13 12:51 
"""
import time
import logging
from functools import wraps
from hard_connect.hard_conn import hard_conn as HardConnect


def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer


def receive_generator():
    while True:
        data = yield
        print('Data:', data)


def socket_send_eg():
    """
    Example of sending data using socket
    :return:
    """
    hard = HardConnect(conn_type='socket', ip='127.0.0.1', port=60000)
    hard.send('>vcm upload(on)')


def socket_send_receive_eg():
    """
    Example of sending and receiving data using socket
    :return:
    """
    hard = HardConnect(conn_type='socket', ip='127.0.0.1', port=60000)
    receive_data = hard.send_receive('>vcm upload(on)')
    print(receive_data)


def socket_receive_data_with_threading():
    """
    Example of receiving data using socket with threading

    Receive data and put it in a fifo queue
    :return:
    """
    hard = HardConnect(conn_type='socket', ip='127.0.0.1', port=60000)
    hard.start()


def socket_receive_data_with_coroutine():
    """
    Example of receiving data using socket with coroutine

    Receive data and send to a generator
    :return:
    """
    recv = receive_generator()
    next(recv)
    hard = HardConnect(conn_type='socket', ip='127.0.0.1', port=60000, receive_generator=recv)


def socket_connect_set_log_level_and_log_filename():
    """
    Log config is log.py file

    Default log level is logging.INFO
    logging.INFO: use StreamHandler, log to console
    logging.DEBUG: use FileHandler, log to file and console, file name is hard_connect.log in the current directory
    :return:
    """
    hard = HardConnect(
        conn_type='socket', ip='127.0.0.1', port=60000,
        logging_level=logging.DEBUG,
        # logging_filename='/tmp/hard_conn.log'
    )
    hard.send('>vcm upload(on)')


def test_conn():
    # hard = HardConnect(
    #     conn_type='socket', ip='127.0.0.1', port=60000,
    #     # logging_filename='/tmp/hard_conn.log'
    # )

    # hard = HardConnect(conn_type='socket', ip='127.0.0.1', port=60000, logging_level=logging.INFO)
    # hard = HardConnect(conn_type='socket', ip='192.168.0.100', port=5000, logging_level=logging.INFO)
    # hard1 = HardConnect(
    #     conn_type='socket', ip='192.168.0.100', port=5001,  receive_generator=recv_gen
    # )
    hard = HardConnect(
        conn_type='serial', device='/dev/tty.usbmodem1402',
        baud_rate=115200, is_read_line=True
    )
    hard.start()

    data = hard.send_receive('>vcm force(10)')
    # print('----', hard.send_receive('>vcm force(10)'))
    time.sleep(1)
    # print('----', hard.send_receive('>vcm force(10)'))
    # print(hard.send_receive('>vcm force(10)'))
    # hard.send('>vcm force(50)')
    # hard.send_receive('>vcm force(100)')
    # hard.send('>vcm force(0)')
    pass


if __name__ == '__main__':
    test_conn()
