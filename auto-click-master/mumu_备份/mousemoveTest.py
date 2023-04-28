import time
import ctypes
import ctypes.wintypes

# 定义常量
HWND = 264114  # Windows 记事本应用程序的窗口句柄
WM_LBUTTONDOWN = 0x0201  # 鼠标左键按下消息
WM_MOUSEMOVE = 0x0200  # 鼠标移动消息
WM_LBUTTONUP = 0x0202  # 鼠标左键松开消息


# 获取坐标函数
def get_point(x, y):
    return x | y << 16


# 构造消息函数
def send_message(hwnd, msg, wparam, lparam):
    result = ctypes.windll.user32.SendMessageW(hwnd, msg, wparam, lparam)
    if result == 0:
        raise Exception("发送消息失败")


# 获取窗口位置函数
def get_window_rect(hwnd):
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


# 获取窗口大小函数
def get_window_size(hwnd):
    left, top, right, bottom = get_window_rect(hwnd)
    width = right - left
    height = bottom - top
    return width, height


# 获取窗口中心点函数
def get_window_center(hwnd):
    width, height = get_window_size(hwnd)
    left, top, _, _ = get_window_rect(hwnd)
    center_x = left + width // 2
    center_y = top + height // 2
    return center_x, center_y


# 模拟鼠标拖动函数
def drag_window(hwnd):
    # 获取窗口中心点坐标
    center_x, center_y = 834, 17

    # 发送鼠标左键按下消息
    point = get_point(center_x, center_y)
    send_message(hwnd, WM_LBUTTONDOWN, 0, point)

    # 发送鼠标移动消息
    for i in range(10):
        send_message(hwnd, WM_MOUSEMOVE, 0, get_point(center_x + i * 10, center_y))
        time.sleep(0.3)

    # 发送鼠标左键松开消息
    send_message(hwnd, WM_LBUTTONUP, 0, point)


# 测试代码
if __name__ == '__main__':
    time.sleep(3)  # 等待 Windows 记事本应用程序启动
    drag_window(394868)  # 拖动窗口
