# 实现自动挂机刷技能 原理：鼠标来回拖动
# 1.屏幕缩放调为100%
# 2.模拟器分辨率1280x720
# 3. 按下esc停止挂机
# 4. 模拟器不可以最小化或者拖出屏幕
import random
import threading
import time
from ctypes import windll

import win32gui
from pynput import keyboard

import mumu_core
import mumu_RecordClickByPyautogui
import mumu_PIcContrastToClick
import mumu_ReadClickByPyautogui
import mumu_RecordToClick
import mumu_AutoArena  # 引用部分功能

autoflag = True  # 自动走路
speedflag = True  # 双击快进
battleflag = False  # 战斗结束面板
threadflag = True  # 最外层循环标识

core = mumu_core.Core()
handle = windll.user32.FindWindowW(None, "MuMu模拟器12")
controls = []
win32gui.EnumChildWindows(handle, core.callback, controls)
for control in controls:
    print(control)

leftbefore = 210, 510
leftafter = 200, 510
rightbefore = 900, 510
rightafter = 1200, 510


def on_press(key):
    if key.name == 'esc':
        print(
            '-----------------------ESC key pressed 本次战斗结束后将终止--------------------------------------------------.')
        global threadflag, autoflag, battleflag, speedflag
        threadflag = False
        autoflag = False
        battleflag = False
        speedflag = False
        listener.stop()


listener = keyboard.Listener(on_press=on_press)  # 开启键盘事件监听
listener.start()


def move():
    # 实现来回移动
    while threadflag:
        while autoflag:
            point1 = mumu_AutoArena.set_random(leftbefore[0], leftbefore[1])
            point2 = mumu_AutoArena.set_random(leftafter[0], leftafter[1])

            core.left_down(controls[0], int(point1[0]), int(point1[1]))  # 鼠标按下，为拖动做准备
            time.sleep(1)
            # 两种方式的对比总结
            # 共同点：都可以实现鼠标的拖动效果
            # 不同点：小幅度多次移动，和一次移动到位。第一种更接近人的操作
            # 注意点：down，move-down，move，down，up 是一次完整的拖拽操作
            # 如果缺少了up，则会导致下一次的点击出现问题，原因是没有抬起鼠标，就再次按下，抬起鼠标，此次操作会丢失
            # 第一种方式 多次小幅移动
            for i in range(4):  # 通过配合time.sleep可以实现持续拖动（拖动图标的动画）
                core.move_to(controls[0], int(point2[0]) - 40 * (i + 1), int(point2[1]))  # 如果每次移动的像素点数过小，会导致不能很快的跑起来
                core.left_down(controls[0], int(point2[0]) - 40 * (i + 1), int(point2[1]))
                # time.sleep(0.3)  # 不等待时间也可以实现跑步，时间过长反而会打断跑步
            core.left_up(controls[0], int(point2[0]) - 40 * 4, int(point2[1]))  # 有无此行貌似无影响

            # 第二种方式 一次移动到位
            # core.move_to(controls[0], int(point2[0]) - 100, int(point2[1]))
            # core.left_down(controls[0], int(point2[0]) - 100, int(point2[1]))
            # core.left_up(controls[0], int(point2[0]) - 100, int(point2[1]))

            time.sleep(5 + random.uniform(0.1, 1))

            point3 = mumu_AutoArena.set_random(rightbefore[0], rightbefore[1])
            point4 = mumu_AutoArena.set_random(rightafter[0], rightafter[1])

            core.left_down(controls[0], int(point3[0]), int(point3[1]))  # 准备动作
            # 第一种方式
            for i in range(4):
                core.move_to(controls[0], int(point4[0]) + (i + 1) * 40, int(point4[1]))
                core.left_down(controls[0], int(point4[0]) + (i + 1) * 40, int(point4[1]))
            # time.sleep(2)
            core.left_up(controls[0], int(point4[0]) + 4 * 40, int(point4[1]))

            # # 第二种方式
            # core.move_to(controls[0], int(point4[0]) + 100, int(point4[1]))
            # core.left_down(controls[0], int(point4[0]) + 100, int(point4[1]))
            # core.left_up(controls[0], int(point4[0]) + 100, int(point4[1]))

            time.sleep(5 + random.uniform(0.1, 1))


def get_image_speedup():
    # 两次单击加速按钮，节省一点点时间
    global autoflag
    global speedflag
    global battleflag
    while threadflag:
        while speedflag:  # 循环进行对比，如果相似度低于0.97就继续循环，高于则退出循环进行点击
            image = core.capture(handle)
            pc = mumu_PIcContrastToClick.PicContrast()  # 坐标对比
            contrastimg = "speedup.png"
            print("speedup--")
            point = pc.get_xy(image, contrastimg)
            if point == 0.001:
                time.sleep(1)
            else:
                autoflag = False
                time.sleep(1.5)  # 等待speedup按钮可点击
                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.6)  # 两次单击的间隔时间，时间不能过短
                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))
                # time.sleep(20)  # 等待角色做好准备
                speedflag = False
                battleflag = True


def gameover_doubleClick():
    # 战斗结束后 点击结算页面 多点击几次，以防止当技能升级时，无法正常退出
    while threadflag:
        global speedflag
        global autoflag
        global battleflag
        while battleflag:  # 循环进行对比，如果相似度低于0.97就继续循环，高于则退出循环进行点击
            image = core.capture(handle)
            pc = mumu_PIcContrastToClick.PicContrast()  # 坐标对比
            contrastimg = "battleResult.png"
            print("battleResult--")
            point = pc.get_xy(image, contrastimg)
            if point == 0.001:
                time.sleep(1)
            else:
                time.sleep(0.4)

                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))

                time.sleep(0.6)

                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))

                time.sleep(0.6)

                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))

                time.sleep(0.6)

                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.6)

                core.left_down(controls[0], int(point[0]), int(point[1]))
                time.sleep(0.1)
                core.left_up(controls[0], int(point[0]), int(point[1]))

                time.sleep(1.2)  # 等待角色做好准备

                autoflag = True
                speedflag = True
                battleflag = False


if __name__ == '__main__':
    move_thread = threading.Thread(target=move)
    get_image_speedup_thread = threading.Thread(target=get_image_speedup)
    gameover_doubleClick_thread = threading.Thread(target=gameover_doubleClick)

    # 启动线程
    move_thread.start()
    get_image_speedup_thread.start()
    gameover_doubleClick_thread.start()

    # 等待三个线程结束
    move_thread.join()
    get_image_speedup_thread.join()
    gameover_doubleClick_thread.join()
