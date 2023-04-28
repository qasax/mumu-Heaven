from pynput import mouse, keyboard

import mumu_RecordClickByPyautogui
import mumu_ReadClickByPyautogui


# 记录鼠标点击坐标时间。
def recordClick(handle, name):
    rd = mumu_RecordClickByPyautogui.RecordMouse(handle, name)
    rd.main()
    print("存储完成")

# 读取鼠标坐标数据
# read = mumu_ReadClickByPyautogui.ReadMouse("mouse_click_log.txt")
# arrays=[]
# read.read_click(arrays)
# print(arrays)
# print(arrays[0]['x'])
