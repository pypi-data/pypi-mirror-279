#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：testbase.py
@Author  ：KING
@Date    ：2024/6/11 11:01 
"""
import time
import unittest
from hard_conn import hard_conn


class TestSocket(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.hard = hard_conn(conn_type='socket', ip='192.168.0.100', port=5000)
        self.hard.start()
        super().__init__(*args, **kwargs)

    def test_send(self):
        self.hard.send('>vcm force(10)')
        time.sleep(1)
        self.assertEqual(self.hard.queue.__len__(), 1)
        self.hard.queue.clear()

    def test_receive(self):
        print(self.hard.queue)
        self.hard.send('>vcm force(10)')
        time.sleep(1)
        self.assertEqual(self.hard.queue.__len__(), 1)

    def __del__(self):
        self.hard.send('>vcm force(0)')


if __name__ == '__main__':
    unittest.main()
