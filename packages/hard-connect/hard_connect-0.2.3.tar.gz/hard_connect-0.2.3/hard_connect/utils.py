#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：dequeue.py
@Author  ：KING
@Date    ：2024/6/11 12:49 
"""
import logging
from typing import Union
from collections import deque
from abc import ABC, abstractmethod
logger = logging.getLogger("hard_conn")


class BaseConn(ABC):
    def __init__(
            self,
            send_lf='\r\n',
            receive_lf='\r\n',
            console_print=True,
            queue_max_length=500,
            timeout: int = 1,
            end_of_msg=None,
            keep_line_feed=False,
    ):
        """
        Base class for communication, including serial, socket, etc.
        :param send_lf:            # send line feed, default: '\r\n'
        :param receive_lf:         # receive line feed, default: '\r\n'
        :param console_print:      # print data to console, default: True
        :param queue_max_length:   # queue max length, default: 500
        :param timeout:            # Send and receive timeout, default: 1s
        :param end_of_msg:         # special line data，if set, discard this data
        :param keep_line_feed:     #  Write queue data to preserve line breaks  default: False
        """
        self.conn = None
        self.send_lf = send_lf
        self.receive_lf = receive_lf
        self.console_print = console_print
        self.end_of_msg = end_of_msg
        self.keep_line_feed = keep_line_feed
        self.timeout = timeout
        self.queue = DequeWithMaxLen(queue_max_length)
        super().__init__()

    def __del__(self):
        """
        close socket connection when object is destroyed
        :return:
        """
        self.disconnect()

    @abstractmethod
    def connect(self):
        """
        connect to the server
        :return:
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        disconnect from the server
        :return:
        """
        pass

    @abstractmethod
    def send(self, send_str: Union[str, bytes]):
        """
        send message to the server
        :param send_str:
        :return:
        """
        pass

    @abstractmethod
    def receive(self):
        """
        receive message from the server
        :return:
        """
        pass

    def put_queue(self, bytes_recv_line: bytes):
        """
        sub thread receive data, put data to queue

        :param bytes_recv_line:
        :return:
        """
        try:
            line = bytes_recv_line.decode()
            if not self.keep_line_feed:
                line = line.strip()   # delete line feed
            self.console_print and print('recv_data:', line)

            if self.end_of_msg and line == self.end_of_msg:
                return
            self.queue.put(line)
        except UnicodeDecodeError as e:
            logger.debug(f'Decode error: {e}', ' Resource Bytes:', repr(bytes_recv_line))
        pass

    def new_value(self, value_index=-1):
        """

        :param value_index: get value from queue, default: -1, get last value
        :return:
        """
        if self.queue.__len__() == 0:
            return None
        return self.queue.get_new_value(value_index)


class DequeWithMaxLen(deque):
    """
    FIFO queue with a maximum length. Default is 500

    If the queue is full, the oldest item will be removed.

    put: Put a new value in the queue
    popleft: Remove and return the leftmost item
    get: Alias of popleft
    get_new_value: Get Queue right value, but not remove it
    clear(): Clear the queue
    copy(): Return a shallow copy of the queue
    count(x): Return the number of items in the queue
    extend(iterable): Extend the right side of the queue by appending elements from the iterable
    """
    def __init__(
            self, max_length=500
    ):
        self.max_length = max_length
        super().__init__(maxlen=self.max_length)

    def put(self, item):
        if len(self) == self.max_length:
            self.popleft()
        self.append(item)

    def popleft(self):
        """
        Remove and return the leftmost item.
        :return:
        """
        return super().popleft()
    
    def get(self):
        return self.popleft()

    def get_new_value(self, value_index=-1):
        """
        Get Queue right value, but not remove it
        :return:
        """
        if len(self) == 0:
            return None
        return self[value_index]
