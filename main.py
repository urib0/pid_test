#!/usr/bin/env python3

import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# シリアルポートの設定
port = "/dev/tty.usbmodem143301"  # 使用しているシリアルポートに応じて変更
baudrate = 115200

ser = serial.Serial(port, baudrate, timeout=0.2)

# グラフ設定
plt.ion()  # インタラクティブモードオン
fig, ax = plt.subplots()
line, = ax.plot([], [])

# 5分間のデータポイント数
data_points = 5 * 60 * 5  # 5分 x 60秒 x 5データ/秒
temperature_data = deque([0] * data_points, maxlen=data_points)
time_data = deque(np.linspace(-300, 0, data_points), maxlen=data_points)

def update_graph(new_temp):
    temperature_data.append(new_temp)
    line.set_xdata(time_data)
    line.set_ydata(temperature_data)

    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(1)

try:
    while True:
        data = ser.readline().strip()
        if data:
            print(f"{data=}")
            try:
                temperature = float(data)
                update_graph(temperature)
            except ValueError:
                print(f"Invalid data: {data}")
finally:
    ser.close()
    plt.ioff()
    plt.show()
