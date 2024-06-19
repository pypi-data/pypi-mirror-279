#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：test_serial.py
@Author  ：KING
@Date    ：2024/6/11 19:37 
"""
import time
import unittest
from hard_conn import hard_conn


class TestSerial(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.hard = hard_conn(conn_type='serial', device='/dev/tty.usbserial-110')
        self.hard.start()
        super().__init__(*args, **kwargs)

    def test_send(self):
        self.hard.send('>vcm current(0.3)')
        time.sleep(1)
        self.assertEqual(self.hard.queue.__len__(), 1)
        self.hard.queue.clear()

    def test_receive(self):
        print(self.hard.queue)
        self.hard.send('>vcm current(0.4)')
        time.sleep(1)
        self.assertEqual(self.hard.queue.__len__(), 1)

    def __del__(self):
        self.hard and self.hard.send('>vcm current(0)')


if __name__ == '__main__':
    unittest.main()
