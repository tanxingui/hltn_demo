import threading
import random


class shared(object):

    def __init__(self, x=0):
        # Created a Lock object
        self.lock = threading.Lock()
        self.incr = x

        # Increment function for the thread

    def incrementcounter(self):
        print("等待开锁")
        # Lock acquired by the current thread
        self.lock.acquire()
        try:
            print('已获取锁，当前计数器值:', self.incr)
            self.incr = self.incr + 1
        finally:
            print('锁已释放，当前计数器值:', self.incr)
            # Lock released by the given thread
            self.lock.release()


def helper_thread(c):
    # Getting a random integer between 1 to 3
    r = random.randint(1, 3)
    print("选择的随机值:", r)
    for i in range(r):
        c.incrementcounter()
    print('已完成', str(threading.current_thread().getName()))
    print()


if __name__ == '__main__':
    obj = shared()

    thread1 = threading.Thread(target=helper_thread, args=(obj,))
    thread1.start()

    thread2 = threading.Thread(target=helper_thread, args=(obj,))
    thread2.start()

    thread1.join()
    thread2.join()

    print('最终计数的值:', obj.incr)
print('aaa')
