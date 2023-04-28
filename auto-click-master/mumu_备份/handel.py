import psutil
import time
import win32api
import win32gui
import win32process

time.sleep(1)
point = win32api.GetCursorPos()
hwnd = win32gui.WindowFromPoint(point)
print(hwnd)  # 1050276
# 通过句柄获取【线程ID 进程ID】
hread_id, process_id = win32process.GetWindowThreadProcessId('1050276')
# 通过进程ID获取【进程名称】 列：weixin.exe
process = psutil.Process(process_id).name()
# 通过进程ID 获取主文件程序【标准路径】 列：D:/filed/windoee/weixin.exe
p_bin = psutil.Process(process_id).exe()
print(process)
