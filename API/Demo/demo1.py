# def iterator():
#     for i in range(1, 3):
#         yield i * i  # 第一种实现方法
#
#
# b = iterator()
# print(type(b))  # <class 'generator'>
# for i, x in enumerate(b):
#     print(str(i + 1) + "²", x)  # 输出1² 1   2² 4

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


# import os
#
# def print_all_files(file_path):
#     for item in os.scandir(file_path):
#         if item.is_file():
#             print(item.path)
#         elif item.is_dir():
#             print_all_files(item.path)
#
# print_all_files('D:\欢乐童年脚本')

# 回调
# def huitiao(abc, bb):
#     print(f'a * b的结果是 --> {abc}    {bb}')
#
#
# def main1(a, b, fac):
#     aa = a * b
#     return fac(aa, '√')
#
#
# if __name__ == '__main__':
#     main1(2, 3, huitiao)

# 闭包


# def logger(fac):
#     def neizhi(*args, **kwargs):
#         print(f'调用函数的是 --> {fac.__name__}')
#         start_time = time.time()
#         result = fac(*args, **kwargs)
#         end_time = time.time()
#         Time = end_time - start_time
#         print(f"'{fac.__name__}'函数的执行时间是 --> {Time:.2f}秒")
#         print(f'结果是 --> {result}')
#
#     return neizhi
#
#
# @logger
# def abc(x, y, n, v):
#     time.sleep(0.5)
#     return x * y * n * v
#
#
# abc(2, 3, 2, 4)






# class B():
#     g = 55
#
#     def run2(self):
#         print(8888888888888888888888888888888)
#
# # 创建类A
# class A():
#     def __new__(cls, *args, **kwargs):
#
#         return object.__new__(B, *args, **kwargs)  # 传参传的其他类对象B，最后return返回B类对象实例，可调用B类的方法、属性
#
#     def __init__(self):
#        self.a = 2
#        self.b = 3
#
#     def run(self):
#         print(222222222222222222222222)
#
# aaa = A()
# bbb = A()
#
# print(aaa is bbb)
#
# print(bbb.g)
# bbb.run2()



