from pynput import mouse, keyboard
import time
import pyperclip

# 记录鼠标点击事件的列表
click_events = []


# 定义鼠标点击事件的回调函数
def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        # 记录当前系统时间和鼠标指针当前位置
        click_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        click_position = f'x={x} y={y}'
        click_events.append((click_time, click_position))
        print(f'Clicked at {click_time} ({click_position})')

        # 如果同时按下了Ctrl键，则复制当前位置所在的单词到剪贴板中
        if pressed == True and keyboard_controller.ctrl_pressed == True:
            current_word = get_current_word()
            pyperclip.copy(current_word)


# 获取当前鼠标指针所在的单词
def get_current_word():
    # 读取最近一次记录的鼠标位置
    last_event = click_events[-1][1]
    last_x, last_y = last_event.split(' ')

    # 移动鼠标指针到最近一次记录的位置，并模拟按下Ctrl+C
    mouse_controller.position = (int(last_x[2:]), int(last_y[2:]))
    mouse_controller.click(mouse.Button.left, 1)
    keyboard_controller.press(keyboard.Key.ctrl)
    keyboard_controller.press('c')
    time.sleep(0.1)
    keyboard_controller.release('c')
    keyboard_controller.release(keyboard.Key.ctrl)

    # 从剪贴板中读取复制的单词并返回
    return pyperclip.paste().strip()


# 创建鼠标控制器和键盘控制器对象
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

# 监听鼠标点击事件
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
