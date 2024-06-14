#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：base_socket.py
@Author  ：KING
@Date    ：2024/6/11 09:48 
"""
import time
import socket
import logging
from typing import Union
from hard_connect.utils import BaseConn
from abc import abstractmethod
logger = logging.getLogger("hard_conn")


class BaseSocket(BaseConn):
    """
    Base socket class.
    init socket and connect, destroy socket and disconnect
    implement send_cmd and recv_msg, Subclass must implement these two methods.

    Don't set timeout, if you set timeout, you will set block mode to blocking mode. Keep socket the default value.
    """
    def __init__(
            self,
            ip, port,
            **kwargs
    ):
        """
        :param ip:   socket connect ip
        :param port: socket connect port
        """
        super().__init__(**kwargs)
        self.ip = ip
        self.port = port if isinstance(port, int) else int(port)
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.ip, self.port))
            self.timeout and self.conn.settimeout(self.timeout)
        except Exception as e:
            raise e

    def disconnect(self):
        self.conn and self.conn.close()

    @abstractmethod
    def send(self, send_str: Union[str, bytes]):
        """
        send message to socket server,
        message: message + line break
        :param send_str:
        :return: None
        """
        pass

    @abstractmethod
    def receive(self, length: int = 1024):
        """
        receive message from socket server, Default length is 1024
        :param length:
        :return:
        """
        pass


class SocketConn(BaseSocket):
    """
    Implementing send and receive methods


    """
    def __init__(
            self,
            ip: str,
            port: int,
            **kwargs
    ):
        super().__init__(ip, port, **kwargs)

    def send(self, send_str: Union[str, bytes]):
        """
        send message to socket server.

        :param send_str:
        :return:
        """
        if not self.conn:
            raise Exception(f"socket {self.ip}:{self.port} is not connected")

        try:
            if isinstance(send_str, bytes):
                self.conn.sendall(send_str)
                self.console_print and print(f'send bytes length: {len(send_str)}')
            else:
                send_msg = send_str + self.send_lf
                self.console_print and print(f'send: {send_msg}')
                self.conn.sendall(send_msg.encode())
        except Exception as e:
            logger.debug(f"send socket {self.ip}:{self.port} error: {e}")

    def receive(
            self, length: int = 1024,
            waiting_data: bytes = None,
            receive_length: int = None,
    ) -> Union[bytes, None]:
        """
        receive message from socket server, Default length is 1024

        Process multi-line data, Process coding is bytes, not str
        The received data may be incomplete or line by line, so we need to process it line by line

        Loop waiting data,
        Return the received data when waiting_data is not None or timeout is reached

        If set receive_length
        When the received data is greater than or equal to receive_length, return the received data
        :param length:
        :param waiting_data:
        :param receive_length:
        :return:
        """
        bytes_line_break = self.receive_lf.encode()
        bytes_end_of_msg = self.end_of_msg.encode()

        socket_data = b''
        try:
            while self.conn:
                bytes_recv_data = self.conn.recv(length)
                socket_data += bytes_recv_data

                # send command and waiting for server response data
                if waiting_data is not None:
                    waiting_data += bytes_recv_data

                # Data write queue by line
                if bytes_line_break in socket_data:

                    # delete empty line
                    lines = [_line for _line in socket_data.split(bytes_line_break) if len(_line)]
                    if len(lines) == 0:
                        socket_data = b''
                    elif len(lines) == 1:
                        self.put_queue(lines[0])
                        socket_data = b''
                    else:
                        socket_data = lines[-1]
                        for line in lines[:-1]:
                            self.put_queue(line + bytes_line_break)

                # when waiting_data is not None. First data put queue then return data, end receive of loop
                if ((waiting_data and bytes_end_of_msg in waiting_data)
                        or (receive_length and len(waiting_data) >= receive_length)):
                    return waiting_data
        except socket.timeout:
            return waiting_data if waiting_data is not None else socket_data
        except Exception as e:
            logger.debug('Socket Exception:', e)

    def send_receive(self, send_str: Union[str, bytes], receive_length=None) -> str:
        """
        send message to socket server and receive message from socket server

        :param send_str:
        :param receive_length:
        :return:
        """
        self.send(send_str)
        receive_data = b''
        receive_data = self.receive(
            length=1024, waiting_data=receive_data, receive_length=receive_length
        )
        return receive_data.decode().strip() if receive_data else None
