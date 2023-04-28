def method1():
    print("This is method 1")

def method2():
    print("This is method 2")

def method3():
    print("This is method 3")

# 使用字典来存储选项
options = {
    1: method1,
    2: method2,
    3: method3
}

# 获取用户输入
user_input = int(input("请输入一个数字（1-3）："))

# 获取相应的函数并调用
func = options.get(user_input)
if func:
    func()
else:
    print("输入不合法")
