# 读取存储在文本里的鼠标点击信息

class ReadMouse:
    def __init__(self, name):
        self.name = name

    def read_click(self, arrays=[]):
        # 打开文本文件并读取内容
        with open("./mumu_action/" + self.name, 'r') as f:
            content = f.readlines()
            # 循环遍历每一行内容
            for line in content:
                # 使用字符串分割函数获取鼠标坐标和时间戳
                x, y, timestamp = line.split(',')[0].split('(')[1], line.split(',')[1].split(')')[0], \
                    line.split('Timestamp: ')[1].strip()
                print('原始数据--Mouse position in app window: ({}, {}), Timestamp: {}'.format(x, y, timestamp))
                arrays.append({'x': x, 'y': y, 'timestamp': timestamp})

