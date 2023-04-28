from ctypes import c_ubyte
from ctypes import windll, byref

import numpy as np
import string
import time
import win32gui
from ctypes.wintypes import HWND
from ctypes.wintypes import RECT, POINT


# 核心功能库 实现鼠标点击 按键 功能 后台截图的功能

class Core():
    PostMessageW = windll.user32.PostMessageW
    ClientToScreen = windll.user32.ClientToScreen

    WM_MOUSEMOVE = 0x0200
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    WM_MOUSEWHEEL = 0x020A
    WHEEL_DELTA = 120
    GetDC = windll.user32.GetDC
    CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
    GetClientRect = windll.user32.GetClientRect
    CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
    SelectObject = windll.gdi32.SelectObject
    BitBlt = windll.gdi32.BitBlt
    SRCCOPY = 0x00CC0020
    GetBitmapBits = windll.gdi32.GetBitmapBits
    DeleteObject = windll.gdi32.DeleteObject
    ReleaseDC = windll.user32.ReleaseDC

    # 排除缩放干扰
    windll.user32.SetProcessDPIAware()

    PostMessageW = windll.user32.PostMessageW
    MapVirtualKeyW = windll.user32.MapVirtualKeyW
    VkKeyScanA = windll.user32.VkKeyScanA

    WM_KEYDOWN = 0x100
    WM_KEYUP = 0x101

    # https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    VkCode = {
        "back": 0x08,
        "tab": 0x09,
        "return": 0x0D,
        "shift": 0x10,
        "control": 0x11,
        "menu": 0x12,
        "pause": 0x13,
        "capital": 0x14,
        "escape": 0x1B,
        "space": 0x20,
        "end": 0x23,
        "home": 0x24,
        "left": 0x25,
        "up": 0x26,
        "right": 0x27,
        "down": 0x28,
        "print": 0x2A,
        "snapshot": 0x2C,
        "insert": 0x2D,
        "delete": 0x2E,
        "lwin": 0x5B,
        "rwin": 0x5C,
        "numpad0": 0x60,
        "numpad1": 0x61,
        "numpad2": 0x62,
        "numpad3": 0x63,
        "numpad4": 0x64,
        "numpad5": 0x65,
        "numpad6": 0x66,
        "numpad7": 0x67,
        "numpad8": 0x68,
        "numpad9": 0x69,
        "multiply": 0x6A,
        "add": 0x6B,
        "separator": 0x6C,
        "subtract": 0x6D,
        "decimal": 0x6E,
        "divide": 0x6F,
        "f1": 0x70,
        "f2": 0x71,
        "f3": 0x72,
        "f4": 0x73,
        "f5": 0x74,
        "f6": 0x75,
        "f7": 0x76,
        "f8": 0x77,
        "f9": 0x78,
        "f10": 0x79,
        "f11": 0x7A,
        "f12": 0x7B,
        "numlock": 0x90,
        "scroll": 0x91,
        "lshift": 0xA0,
        "rshift": 0xA1,
        "lcontrol": 0xA2,
        "rcontrol": 0xA3,
        "lmenu": 0xA4,
        "rmenu": 0XA5
    }

    def move_to(self, handle: HWND, x: int, y: int):
        """移动鼠标到坐标（x, y)

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
        wparam = 0
        lparam = y << 16 | x
        print("本次鼠标移动至的坐标为")
        print(x, y)
        self.PostMessageW(handle, self.WM_MOUSEMOVE, wparam, lparam)

    def left_down(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)按下鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
        print("本次鼠标左键按下对应的坐标为")
        print(x, y)
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(handle, self.WM_LBUTTONDOWN, wparam, lparam)

    def left_up(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)放开鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
        print("本次鼠标左键抬起对应的坐标为")
        print(x, y)
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(handle, self.WM_LBUTTONUP, wparam, lparam)

    def scroll(self, handle: HWND, delta: int, x: int, y: int):
        """在坐标(x, y)滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            delta (int): 为正向上滚动，为负向下滚动
            x (int): 横坐标
            y (int): 纵坐标
        """

        self.move_to(handle, x, y)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
        wparam = delta << 16
        p = POINT(x, y)
        self.ClientToScreen(handle, byref(p))
        lparam = p.y << 16 | p.x
        self.PostMessageW(handle, self.WM_MOUSEWHEEL, wparam, lparam)

    def scroll_up(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)向上滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        print("本次鼠标向上滚动对应的坐标及偏移量为")
        print(x, y, self.WHEEL_DELTA)
        self.scroll(handle, self.WHEEL_DELTA, x, y)

    def scroll_down(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)向下滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        print("本次鼠标向下滚动对应的坐标及偏移量为")
        print(x, y, self.WHEEL_DELTA)
        self.scroll(handle, -self.WHEEL_DELTA, x, y)

    def capture(self, handle: HWND):
        """窗口客户区截图

        Args:
            handle (HWND): 要截图的窗口句柄

        Returns:
            numpy.ndarray: 截图数据
        """
        # 获取窗口客户区的大小
        r = RECT()
        self.GetClientRect(handle, byref(r))
        width, height = r.right, r.bottom
        # 开始截图
        dc = self.GetDC(handle)
        cdc = self.CreateCompatibleDC(dc)
        bitmap = self.CreateCompatibleBitmap(dc, width, height)
        self.SelectObject(cdc, bitmap)
        self.BitBlt(cdc, 0, 0, width, height, dc, 0, 0, self.SRCCOPY)
        # 截图是BGRA排列，因此总元素个数需要乘以4
        total_bytes = width * height * 4
        buffer = bytearray(total_bytes)
        byte_array = c_ubyte * total_bytes
        self.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        self.DeleteObject(bitmap)
        self.DeleteObject(cdc)
        self.ReleaseDC(handle, dc)
        # 返回截图数据为numpy.ndarray
        return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

    def callback(self, hwnd, controls):
        controls.append(hwnd)

    def get_virtual_keycode(self, key: str):
        """根据按键名获取虚拟按键码

        Args:
            key (str): 按键名

        Returns:
            int: 虚拟按键码
        """
        if len(key) == 1 and key in string.printable:
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
            return self.VkKeyScanA(ord(key)) & 0xff
        else:
            return self.VkCode[key]

    def key_down(self, handle: HWND, key: str):
        """按下指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.get_virtual_keycode(key)
        scan_code = self.MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        print("本次按下的键盘按键为")
        print(vk_code)
        wparam = vk_code
        lparam = (scan_code << 16) | 1
        self.PostMessageW(handle, self.WM_KEYDOWN, wparam, lparam)

    def key_up(self, handle: HWND, key: str):
        """放开指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.get_virtual_keycode(key)
        scan_code = self.MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        print("本次抬起的键盘按键为")
        print(vk_code)
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        self.PostMessageW(handle, self.WM_KEYUP, wparam, lparam)


if __name__ == "__main__":
    # import sys
    # if not windll.shell32.IsUserAnAdmin():
    # 不是管理员就提权
    # windll.shell32.ShellExecuteW(
    # None, "runas", sys.executable, __file__, None, 1)
    core = Core()
    import cv2

    handle = windll.user32.FindWindowW(None, "MuMu模拟器12")
    controls = []
    win32gui.EnumChildWindows(handle, core.callback, controls)
    print("句柄"+str(handle)+"的子句柄为")
    for control in controls:
        print(control)

    # 截图时要保证游戏窗口的客户区大小是1334×750
    image = core.capture(handle)
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.imread('./static/game.png', cv2.IMREAD_UNCHANGED)
    # 取出Alpha通道
    alpha = template[:, :, 3]
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = top_left[0] + w, top_left[1] + h
    # 在窗口截图中匹配位置画红色方框
    cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
    cv2.imshow('Match Template', image)
    cv2.waitKey()

    core.left_down(controls[0], 181, 380)
    time.sleep(0.1)
    core.left_up(controls[0], 181, 380)
    time.sleep(0.1)

    # 控制角色向前移动两秒
    # key_down(controls[1], 'w')
    # time.sleep(0.3)
    # key_up(controls[1], 'w')
    # time.sleep(0.3)
    # left_down(controls[1], 70, 280)
    # time.sleep(0.1)
    # left_up(controls[1], 70, 280)
    # time.sleep(2)
    # # 滚动线路列表
    # scroll_down(handle, 170, 188)
