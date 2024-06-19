#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：hard_conn.py
@Author  ：KING
@Date    ：2024/6/11 11:46 
"""
from threading import Thread
from hard_connect.base_socket import SocketConn
from hard_connect.base_serial import SerialConn


class HardConnSock(SocketConn, Thread):
    """
    Connect hard device, socket or serial

    Main thread process send, sub thread process receive

    Receive data put in queue, main thread get data from queue

    """
    def __init__(
            self,
            ip=None,            # ip address, if conn_type is socket, ip is necessary
            port=None,          # port, if conn_type is socket, port is necessary
            daemon=True,
            **kwargs
    ):
        self.ip = ip
        self.port = port
        self.kwargs = kwargs
        super().__init__(self.ip, self.port, **self.kwargs)
        self.daemon = daemon

    def run(self):
        self.receive()


class HardConnSerial(SerialConn, Thread):
    """
    Connect hard device, socket or serial

    Main thread process send, sub thread process receive

    Receive data put in queue, main thread get data from queue

    """
    def __init__(
            self,
            device=None,        # device, if conn_type is serial, device is necessary
            baud_rate=None,     # baud rate, if conn_type is serial, baud rate is necessary
            timeout=1,          # timeout, default: 1s, if conn_type is serial, timeout is available
            daemon=True,
            **kwargs
    ):
        self.device = device
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.kwargs = kwargs
        super().__init__(self.device, self.baud_rate, self.timeout, **self.kwargs)
        self.daemon = daemon

    def run(self):
        self.receive()


def hard_conn(
        conn_type,
        ip=None,
        port=None,
        device=None,
        baud_rate=115200,
        end_of_msg='🔚',
        **kwargs
):
    """
    Connect hard with socket or serial.
    Use the same package to communicate.
    Developers do not need to worry about connections and disconnections， etc.
    Save row data to queue.

    Optional arguments (Other parameters):
    logging_level:  Logging level, default: logging.INFO, DEBUG: write file and console, INFo: write console
    keep_line_feed: Write queue data to preserve line breaks  default: False
    send_lf:        end data with additional terminator. Default \r\n
    receive_lf:     receive data line separator, Default \r\n
    timeout:        timeout, default: 1s,

    For example function:
        send:
        receive:

    :param conn_type:     # hard connect is socket or serial, Only supports socket serial
    :param ip:            # ip address, if conn_type is socket, ip is necessary
    :param port:          # port, if conn_type is socket, port is necessary
    :param device:        # device, if conn_type is serial, device is necessary
    :param baud_rate:     # baud rate, if conn_type is serial, baud rate is necessary. Default: 115200

    :param end_of_msg     # special tag data, Set the tag end_of_msg, which is not stored in the queue. Default  🔚
                          # IF end_of_msg set None or '', No processing of data
                          # The server returns the end of the data after sending the command.
                          # It has no special meaning and is not stored in the queue.
    :param kwargs:        # Other parameters
    :return:
    """
    assert conn_type in ['socket', 'serial'], 'conn_type must be socket or serial'

    kwargs['end_of_msg'] = end_of_msg
    if conn_type == 'socket':
        return HardConnSock(ip, port, **kwargs)
    elif conn_type == 'serial':
        return HardConnSerial(device, baud_rate, **kwargs)


