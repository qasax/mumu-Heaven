# 实现竞技场自动挂机
# 1.屏幕缩放调为100%
# 2.模拟器分辨率1280x720
# 3.先进行操作录入 文件被保存到mumu_action
# 4.然后进行再读取操作，文件名需要带后缀。将界面点击到出击界面。
# 4.模拟器不可以最小化或者拖出屏幕
import random
import time
from ctypes import windll
import win32gui
from pynput import keyboard
import mumu_RecordToClick
import mumu_core
import mumu_PIcContrastToClick
import mumu_ReadClickByPyautogui

autoflag = True  # 是否循环标识



def saveClick(handle, name):
    #保存鼠标点击坐标信息
    # name="mouse_click_log.txt"
    mumu_RecordToClick.recordClick(handle, name)


def readClick(name, arrays: []):
    #读取鼠标点击坐标信息
    return mumu_ReadClickByPyautogui.ReadMouse(name).read_click(arrays)


def set_random(x, y):  # 范围内随机点击
    x = random.uniform(x+5 , x+5 )
    y = random.uniform(y+5, y+5 )
    return x, y


def repeatClick(arrays: [], handle):  # 将录制好的操作进行重放
    i = -1
    flag=0
    for array in arrays:
        if i == -1:
            time.sleep(random.uniform(0.5, 0.9))
            i += 1
            x = int(array['x'])
            y = int(array['y'])
            flag = int(array['timestamp'])
            point = set_random(x, y)  # 随机点击
            core.left_down(handle, int(point[0]), int(point[1]))
            time.sleep(0.03)
            core.left_up(handle, int(point[0]), int(point[1]))
        else:
            i += 1
            time.sleep(int(arrays[i]['timestamp'])-flag + random.uniform(0.3, 0.5))  # 均匀的隔开点击时间
            print("间隔时间为")
            print(int(arrays[i]['timestamp'])-flag)
            flag = int(array['timestamp'])

            x = int(array['x'])
            y = int(array['y'])
            point = set_random(x, y)  # 随机点击
            core.left_down(handle, int(point[0]), int(point[1]))
            time.sleep(0.03)
            core.left_up(handle, int(point[0]), int(point[1]))



def initAction():
    # 进行重复点击操作前的准备 -- 点击开始战斗按钮
    image = core.capture(handle)
    pc = mumu_PIcContrastToClick.PicContrast()  # 坐标对比
    contrastimg = "linkstart.png"
    point = pc.get_xy(image, contrastimg)
    time.sleep(0.3)
    core.left_down(controls[0], int(point[0]), int(point[1]))
    time.sleep(0.1)
    core.left_up(controls[0], int(point[0]), int(point[1]))
    time.sleep(2)
    image = core.capture(handle)
    pc = mumu_PIcContrastToClick.PicContrast()  # 坐标对比
    contrastimg = "gamestart.png"
    point = pc.get_xy(image, contrastimg)
    core.left_down(controls[0], int(point[0]), int(point[1]))
    time.sleep(0.1)
    core.left_up(controls[0], int(point[0]), int(point[1]))
    time.sleep(2)


def speedup():
    #两次点击加速按钮，节省一点时间
    while True:  # 循环进行对比，如果相似度低于0.97就继续循环，高于则退出循环进行点击
        image = core.capture(handle)
        pc = mumu_PIcContrastToClick.PicContrast()  # 坐标对比
        contrastimg = "speedup.png"
        point = pc.get_xy(image, contrastimg)
        if point == 0.001:
            time.sleep(1)
        else:
            time.sleep(0.4)
            core.left_down(controls[0], int(point[0]), int(point[1]))
            time.sleep(0.1)
            core.left_up(controls[0], int(point[0]), int(point[1]))
            time.sleep(0.8)#两次单击间隔时间
            core.left_down(controls[0], int(point[0]), int(point[1]))
            time.sleep(0.1)
            core.left_up(controls[0], int(point[0]), int(point[1]))
            time.sleep(3)  # 等待角色做好准备
            return


def repeatAction():
    #点击再来一次按钮
    while True:
        image = core.capture(handle)
        pc = mumu_PIcContrastToClick.PicContrast()  # 生成类对象以进行坐标对比
        contrastimg = "again.png"
        point = pc.get_xy(image, contrastimg)
        if point == 0.001:
            time.sleep(1)
        else:
            core.left_down(controls[0], int(point[0]), int(point[1]+15))
            time.sleep(0.1)
            core.left_up(controls[0], int(point[0]), int(point[1])+15)
            time.sleep(2)
            return


def on_press(key):#esc退出程序
    if key.name == 'esc':
        print('ESC key pressed.')
        global autoflag
        autoflag = False
        listener.stop()

if __name__ == '__main__':
    core = mumu_core.Core()
    handle = windll.user32.FindWindowW(None, "MuMu模拟器12")
    controls = []
    win32gui.EnumChildWindows(handle, core.callback, controls)
    for control in controls:
        print(control)

    options = {
        1: saveClick,
        2: readClick,
    }

    user_input = int(input("请输入一个数字（1-3）：\n1:操作录制\n2：进行挂机\n"))
    # 获取相应的函数并调用
    func = options.get(user_input)
    if func == saveClick:
        name = str(input("请输入生成文件的名字 \n例如:123.txt\n"))
        print("三秒后开始录制")
        time.sleep(1)
        print(3)
        time.sleep(1)
        print(2)
        time.sleep(1)
        print(1)
        print("操作录制已经开始...")
        func(controls[0], name)
        print("已经存入目标文件" + name)

    elif func == readClick:
        name = str(input("请输入执行文件的名字 \n例如:123.txt\n"))
        print("已经开始执行操作")
        arrays = []
        readClick(name, arrays)
        print("输出储存数据")
        print(arrays)
        for array in arrays:
            print("格式化后数据")
            print(array)
        initAction()  # 初始化操作--进行入场准备
        listener = keyboard.Listener(on_press=on_press)  # 开启键盘事件监听
        listener.start()

        while autoflag:
            speedup()  # 双击快进
            repeatClick(arrays, controls[0])
            repeatAction()  # 循环点击再次战斗
            print("循环完成一次")
    else:
        print("输入不合法")
