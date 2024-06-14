#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：base_serial.py
@Author  ：KING
@Date    ：2024/6/11 09:48 
"""
import time
import serial
import logging
from typing import Union
from abc import abstractmethod
from hard_connect.utils import BaseConn
logger = logging.getLogger("hard_conn")


class BaseSerial(BaseConn):
    def __init__(
        self,
        device,
        baud_rate=115200,
        timeout=1,
        **kwargs
    ):
        """
        Serial communication base class.
        init serial and connect, destroy serial and disconnect
        Subclass must implement these two methods.

        :param device:      serial device, example: /dev/ttyUSB0;
        :param baud_rate:   serial baud rate, default: 115200;
        :param timeout:     timeout, default: 1s;
        """
        super().__init__(**kwargs)
        self.device = device
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.kwargs = kwargs
        self.conn = None
        self.connect()
        self.alive = None

    def connect(self):
        """
        if serial need to set some parameters, you can set it in the kwargs
        :return:
        """
        try:
            self.conn = serial.Serial(
                self.device, self.baud_rate, timeout=self.timeout,
            )
        except Exception as e:
            raise e

    def disconnect(self):
        self.conn and self.conn.close()

    @abstractmethod
    def send(self, send_str: str):
        pass

    @abstractmethod
    def receive(self):
        pass


class SerialConn(BaseSerial):
    """
    Implementing send and receive methods


    """
    def __init__(
            self,
            device: str,
            baud_rate: int,
            timeout: int = 1,
            is_read_line: bool = True,
            **kwargs
    ):
        """

        :param device:       serial device, example: /dev/ttyUSB0;
        :param baud_rate:    serial baud rate, default: 115200;
        :param timeout:      serial timeout, default: 1s;
        :param is_read_line: read row, default: True;
        :param kwargs:
        """
        self.is_read_line = is_read_line
        super().__init__(device, baud_rate, timeout, **kwargs)

    @property
    def is_open(self):
        return self.conn and self.conn.isOpen()

    def send(self, send_str: str):
        if not self.conn or not self.conn.isOpen():
            raise Exception(f"Serial port {self.device} is not connection or open")

        try:
            self.conn.flushInput()  # Clear the input buffer of the serial port
            self.conn.flushOutput()  # clear the output buffer of the serial port

            send_msg = send_str + self.send_lf
            self.console_print and print(f'send: {send_msg}')
            self.conn.write(send_msg.encode())
            self.conn.flush()

        except Exception as e:
            logger.debug(f"send serial {self.device} error: {e}")

    def receive(self, length: int = 1024, waiting_data: bytes = None) -> Union[bytes, None]:
        assert self.is_read_line, 'SerialConn receive method must be read line. Reading by bytes is not supported yet'
        bytes_end_of_msg = self.end_of_msg.encode()
        start_time = time.time() if waiting_data is not None else None
        while True:
            try:
                _bytes = self.conn.readline()
                len(_bytes) and self.put_queue(_bytes)

                # send command and waiting for server response data
                if waiting_data is not None and len(bytes):
                    waiting_data += _bytes
                    if (start_time is not None
                            and (bytes_end_of_msg in waiting_data
                                 or time.time() - start_time > self.timeout)
                    ):
                        return waiting_data
            except Exception as e:
                logger.debug('Serial Exception:', e)
                _bytes = b''
                continue

    def send_receive(self, send_str: Union[str, bytes]) -> str:
        """
        send message to socket server and receive message from socket server

        :param send_str:
        :return:
        """
        self.send(send_str)
        receive_data = b''
        receive_data = self.receive(waiting_data=receive_data).decode()
        return receive_data
