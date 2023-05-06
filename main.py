#!/usr/bin/env python3

import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

INTERVAL = 1
SER_INTERVAL = 0.2
AXYS_TEMP_MIN = 0
AXYS_TEMP_MAX = 250
AXYS_TIME = 3 # 分

# シリアルポートの設定
port = "/dev/tty.usbmodem143301"  # 使用しているシリアルポートに応じて変更
baudrate = 115200

ser = serial.Serial(port, baudrate, timeout=0.2)

# グラフ設定
plt.ion()  # インタラクティブモードオン
fig, ax = plt.subplots()
line, = ax.plot([], [])

# 5分間のデータポイント数
data_points = AXYS_TIME * 60 * int(1/SER_INTERVAL)  # n分 x 60秒 x nデータ/秒
temperature_data = deque([0] * data_points, maxlen=data_points)
time_data = deque(np.linspace(-(AXYS_TIME * 60), 0, data_points), maxlen=data_points)

# 補助線の設定
ax.set_xticks(np.arange(-300, 0, 10))
ax.grid(True)
ax.set_ylim(AXYS_TEMP_MIN,AXYS_TEMP_MAX)

def update_graph(new_temp):
    temperature_data.append(new_temp)
    line.set_xdata(time_data)
    line.set_ydata(temperature_data)

    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.00001)

try:
    while True:
        ser.reset_input_buffer()
        data = ser.readline().strip()
        if data:
            print(f"{data=}")
            try:
                temperature = float(data)
                update_graph(temperature)
            except ValueError:
                print(f"Invalid data: {data}")
        time.sleep(INTERVAL)
finally:
    ser.close()
    plt.ioff()
    plt.show()
