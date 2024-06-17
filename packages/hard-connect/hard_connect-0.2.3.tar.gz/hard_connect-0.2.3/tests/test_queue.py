#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：test_queue.py
@Author  ：KING
@Date    ：2024/6/11 19:21 
"""
import unittest
from hard_connect.utils import DequeWithMaxLen


class TestDequeWithMaxLen(unittest.TestCase):

    def test_init(self):
        # 测试初始化时设置最大长度
        dq = DequeWithMaxLen(max_length=10)
        self.assertEqual(dq.max_length, 10)

    def test_put(self):
        # 测试put方法，包括队列满时移除最旧元素
        dq = DequeWithMaxLen(max_length=3)
        dq.put(1)
        dq.put(2)
        self.assertEqual(list(dq), [1, 2])

        dq.put(3)
        self.assertEqual(list(dq), [1, 2, 3])

        dq.put(4)
        self.assertEqual(list(dq), [2, 3, 4])  # 1被移除

    def test_popleft(self):
        # 测试popleft方法
        dq = DequeWithMaxLen(max_length=5)
        dq.extend([1, 2, 3])
        self.assertEqual(dq.popleft(), 1)
        self.assertEqual(list(dq), [2, 3])

    def test_get(self):
        # 测试get方法，它是popleft的别名
        dq = DequeWithMaxLen(max_length=5)
        dq.extend([1, 2, 3])
        self.assertEqual(dq.get(), 1)

    def test_get_new_value(self):
        # 测试get_new_value方法
        dq = DequeWithMaxLen(max_length=5)
        dq.extend([1, 2, 3])
        self.assertEqual(dq.get_new_value(), 3)
        self.assertEqual(dq.get_new_value(0), 1)  # 测试索引
        self.assertEqual(len(dq), 3)  # 确保元素未被移除

    def test_clear(self):
        # 测试clear方法
        dq = DequeWithMaxLen(max_length=5)
        dq.extend([1, 2, 3])
        dq.clear()
        self.assertEqual(len(dq), 0)

    def test_count(self):
        # 测试count方法
        dq = DequeWithMaxLen(max_length=5)
        dq.extend([1, 2, 2, 3])
        self.assertEqual(dq.count(2), 2)

    def test_extend(self):
        # 测试extend方法
        dq = DequeWithMaxLen(max_length=5)
        dq.extend([1, 2])
        dq.extend([3, 4])
        self.assertEqual(list(dq), [1, 2, 3, 4])

    def test_max_length_behavior(self):
        # 测试最大长度的行为
        dq = DequeWithMaxLen(max_length=2)
        dq.extend([1, 2, 3])
        self.assertEqual(list(dq), [2, 3])  # 1被移除


if __name__ == '__main__':
    unittest.main()
