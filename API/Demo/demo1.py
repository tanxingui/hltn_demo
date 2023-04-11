# def iterator():
#     for i in range(1, 3):
#         yield i * i  # 第一种实现方法
#
#
# b = iterator()
# print(type(b))  # <class 'generator'>
# for i, x in enumerate(b):
#     print(str(i + 1) + "²", x)  # 输出1² 1   2² 4
#
# b1 = (i * i for i in range(1, 3))  # 第二种实现方法，列表推导式的[]变成()会成为generator类
# print(type(b1))  # <class 'generator'>
# for i, x in enumerate(b1):
#     print(str(i + 1) + "²", x)  # 输出1² 1   2² 4

# def factorial(num):
#     # 终止条件，递归到达最小问题（num等于1）时返回1
#     if num == 2:
#         return 2
#     # 如果num不等于1，则递归调用factorial函数，并返回num * factorial(num-1)的结果
#     else:
#         print(num)
#         return num * factorial(num-1)
# print(factorial(4))
import os

import os

def print_all_files(file_path):
    for item in os.scandir(file_path):
        if item.is_file():
            print(item.path)
        elif item.is_dir():
            print_all_files(item.path)

print_all_files('D:\欢乐童年脚本')
