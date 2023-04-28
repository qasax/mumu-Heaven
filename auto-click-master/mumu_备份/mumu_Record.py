import threading
import time

import pyautogui
import win32gui
from pynput import mouse, keyboard
from pynput.mouse import Controller


class RecordMouse():
    # 获取活动窗口句柄
    stop_record = False

    # 获取窗口的位置和尺寸
    def __init__(self, hwnd, name):
        self.keyboard_listener = None
        self.mouse_listener = None
        self.hwnd = hwnd
        self.name = name

    # 鼠标事件处理函数
    def on_click(self, x, y, button, pressed):
        app_x, app_y, app_w, app_h = win32gui.GetWindowRect(self.hwnd)
        if pressed:
            # 判断鼠标事件是否在应用程序窗口内
            if app_x <= x <= app_x + app_w and app_y <= y <= app_y + app_h:
                # 计算鼠标在窗口中的相对坐标，并打印输出
                relative_x, relative_y = x - app_x, y - app_y
                print('Mouse position in app window: ({}, {})'.format(relative_x, relative_y))

                # 获取当前时间戳
                timestamp = int(time.time())

                # 写入文本文件
                with open(self.name, 'a') as f:
                    f.write('Mouse position in app window: ({}, {}), Timestamp: {}\n'.format(relative_x, relative_y,
                                                                                             timestamp))

    # 创建鼠标事件监听器

    # 键盘事件处理函数
    def on_press(self, key):
        global stop_record
        if key == keyboard.Key.esc:
            stop_record = True
            self.keyboard_listener.stop()  # 终止程序
            self.mouse_listener.stop()
            return False

    def main(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()
        self.mouse_listener.join()
        self.keyboard_listener.join()
