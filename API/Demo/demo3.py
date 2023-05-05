# 类装饰器
import time

class Decorator(object):
    def __init__(self, fuc):
        self.fuc = fuc

    def __call__(self, *args, **kwargs):
        print(f'{self.fuc.__name__}函数运行前')
        starttime = time.time()
        result = self.fuc(*args, **kwargs)
        endtime = time.time()
        print(f"{self.fuc.__name__}函数运行后:\n一共用了{(endtime - starttime):.2f}秒")
        return result


@Decorator
def demo(x, y):
    time.sleep(0.2)
    print(x, y)
    return x * y


if __name__ == '__main__':
    print(demo(2, 3))
