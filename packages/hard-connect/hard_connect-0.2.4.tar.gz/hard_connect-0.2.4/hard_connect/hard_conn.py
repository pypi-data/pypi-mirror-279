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
        timeout=1,
        send_lf='\r\n',
        receive_lf='\r\n',
        end_of_msg='🔚',
        keep_line_feed=False,
        **kwargs
):
    """
    Connect hard with socket or serial.
    Use the same package to communicate.
    Developers do not need to worry about connections and disconnections， etc.
    Save row data to queue.

    For example function:
        send:
        receive:

    :param conn_type:     # hard connect is socket or serial, Only supports socket serial
    :param ip:            # ip address, if conn_type is socket, ip is necessary
    :param port:          # port, if conn_type is socket, port is necessary
    :param device:        # device, if conn_type is serial, device is necessary
    :param baud_rate:     # baud rate, if conn_type is serial, baud rate is necessary. Default: 115200
    :param timeout:       # timeout, default: 0.5s,
                          # if conn_type is serial , timeout is available. Default: 1S
    :param send_lf:       # send data with additional terminator. Default \r\n
    :param receive_lf:    # receive data line separator, Default \r\n
    :param end_of_msg     # special tag data, Set the tag end_of_msg, which is not stored in the queue. Default  🔚
                          # IF end_of_msg set None or '', No processing of data
                          # The server returns the end of the data after sending the command.
                          # It has no special meaning and is not stored in the queue.
    :param keep_line_feed: # Write queue data to preserve line breaks  default: False
    :param kwargs:        # Other parameters
    :return:
    """
    assert conn_type in ['socket', 'serial'], 'conn_type must be socket or serial'

    kwargs['timeout'] = timeout
    kwargs['send_lf'] = send_lf
    kwargs['receive_lf'] = receive_lf
    kwargs['end_of_msg'] = end_of_msg
    kwargs['keep_line_feed'] = keep_line_feed
    if conn_type == 'socket':
        return HardConnSock(ip, port, **kwargs)
    elif conn_type == 'serial':
        return HardConnSerial(device, baud_rate, **kwargs)


