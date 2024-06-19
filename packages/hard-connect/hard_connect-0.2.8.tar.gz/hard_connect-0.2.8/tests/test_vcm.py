#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：test_vcm.py
@Author  ：KING
@Date    ：2024/6/17 16:16 
"""
import re
import time
from hard_connect import HardConnect


def get_force(socket5000: HardConnect):
    getdata = socket5000.send_receive(">vcm getforce()")
    if getdata.startswith('<vcm getforce success.'):
        pattern = r'\[([0-9.]+)\s*[a-zA-Z]*\]'
        match = re.search(pattern, getdata)
        if match:
           return match.group(1)
    return None


if __name__ == '__main__':
    vcm_socket5000 = HardConnect(
        conn_type='socket', ip="192.168.0.100", port=5000
    )
    with HardConnect(
        conn_type='socket', ip="192.168.0.100", port=5001, console_print=False,
    ) as vcm_socket5001:
        vcm_socket5001.start()
        vcm_socket5000.send_receive('>vcm upload(on)')

        time.sleep(60)
        exit(1)

    cheng_serial = HardConnect(
        conn_type='serial',
        device='/dev/tty.usbserial-140',
        baud_rate=115200,
        timeout=0.2,
        is_read_line=False,
        length=120,
        console_print=False,
    )
    cheng_serial.start()

    vcm_socket5000.send(">loadcell reset()")
    time.sleep(3)
    text = ['0.20', '0.25', '0.30', '0.35', '0.40']
    pre_vcm_val, pre_cheng_val = 0, 0
    for volt in text:
        vcm_socket5000.send(f'>vcm current({volt})')
        time.sleep(7)

        force = get_force(vcm_socket5000)
        val = cheng_serial.new_value()
        print('force: ', force, '  val: ', val)