import time
from ctypes import windll

import win32gui
import cv2
import mumu_core
import random


# 对比图片寻找目标位置 获取坐标，并且进行随机坐标点击

class PicContrast:
    def get_random_point(self, x1, y1, x2, y2):
        """返回指定两点构成的矩形内的一个随机点"""
        x = random.uniform(min(x1, x2), max(x1, x2))
        y = random.uniform(min(y1, y2), max(y1, y2))
        return int(round(x, 0)), int(round(y, 0))  # 保留两位小数，可根据需要修改--转换为int类型

    def get_xy(self, image, contrastimg):
        # 转为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        # 读取图片，并保留Alpha通道
        template = cv2.imread("./mumu_static/" + contrastimg, cv2.IMREAD_UNCHANGED)
        # 取出Alpha通道
        alpha = template[:, :, 3]
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
        result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
        # 获取结果中最大值和最小值以及他们的坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("相似度")
        print(max_val)
        if 0.986 < max_val <= 1:
            top_left = max_loc
            h, w = template.shape[:2]
            bottom_right = top_left[0] + w, top_left[1] + h
            # 在窗口截图中匹配位置画红色方框
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            # cv2.imshow('Match Template', image)
            # cv2.waitKey()
            print("匹配目标在截图中的左上坐标" + str(top_left))
            print("匹配目标在截图中的右下坐标" + str(bottom_right))
            point = self.get_random_point(top_left[0] + 10, top_left[1] - 30, bottom_right[0] - 10,
                                          bottom_right[1] - 40)
            # 适当缩小点击范围，防止点击不到目标 --根据实际情况调整
            return point
        else:
            return 0.001


if __name__ == '__main__':
    core = mumu_core.Core()
    handle = windll.user32.FindWindowW(None, "MuMu模拟器12")
    controls = []
    win32gui.EnumChildWindows(handle, core.callback, controls)
    for control in controls:
        print(control)

    # 截图时要保证游戏窗口的客户区大小是1334×750
    image1 = core.capture(handle)
    pc = PicContrast()
    contrastimg1 = "gamestart.png"
    point1 = pc.get_xy(image1, contrastimg1)

    core.left_down(controls[0], int(point1[0]), int(point1[1]))
    time.sleep(0.1)
    core.left_up(controls[0], int(point1[0]), int(point1[1]))

    # core.left_down(controls[0], 23, 353)
    # time.sleep(0.1)
    # core.left_up(controls[0], 23, 353)
    # time.sleep(0.1)

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
