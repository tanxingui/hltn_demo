import threading
import time

class CountdownTimer:
    def __init__(self, seconds):
        self.seconds = seconds-1
        self.timer_active = True
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        while self.seconds >= 0 and self.timer_active:
            with self.lock:
                print(f'\r剩余时间：{self.seconds} 秒', end='')
                self.seconds -= 1
                time.sleep(1)
        print("\n倒计时结束！")

    def stop(self):
        self.timer_active = False

# 使用示例
if __name__ == "__main__":
    try:
        countdown_seconds = int(input("请输入倒计时的秒数，按回车键停止倒计时...："))
        timer = CountdownTimer(countdown_seconds)
        timer.start()
        # 倒计时将在后台线程中运行
        input("")
        timer.stop()
    except ValueError:
        print("请输入一个有效的秒数")