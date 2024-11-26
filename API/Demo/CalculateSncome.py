#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/11/18 15:01
# @Author : 新贵大人
描述:
"""

import time,threading,re
from datetime import datetime, timedelta



class WorkdayCalculator:
    def __init__(self, monthly_salary=10000, work_days_month=22, work_hours=7.5):
        self.monthly_salary = monthly_salary
        self.work_days_month = work_days_month
        self.work_hours = work_hours
        self.lunch_break_duration = timedelta(hours=1, minutes=30)  # 午休1小时30分钟
        self.timer_active = True
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self.calculate_earnings).start()

    def stop(self):
        self.timer_active = False

    def input_starttime(self) -> str:
        input_time = input("请输入今日上班打卡时间（格式为HH:MM），按回车结束程序:")
        re_time = re.sub(r'[，.,、。：\s]+', ':', input_time)
        return re_time

    # 一天的收益
    def calculate_daily_wage(self):
        daily_wage = self.monthly_salary / self.work_days_month
        return daily_wage

    # 一小时的收益，需要加上午休1.5
    def calculate_hourly_wage(self):
        hourly_wage = self.calculate_daily_wage() / (self.work_hours + 1.5)
        return hourly_wage

    # 根据上班的时间，计算出下班时间
    def calculate_end_time(self, start_time_str):
        start_time = datetime.strptime(start_time_str, '%H:%M')
        work_hours = self.work_hours + 1.5

        # 计算下班时间
        end_time = start_time + timedelta(hours=work_hours)
        # 上班标准时间
        start_worktime = datetime.strptime('09:30', '%H:%M')
        # 午休时间
        lunch_start = datetime.strptime('12:00', '%H:%M')
        lunch_end = datetime.strptime('13:30', '%H:%M')
        # 如果打卡时间在12:00之前
        if start_time < lunch_start:
            # 如果打卡时间是早上9:30之前，那么下班时间是固定在18:30
            if start_time <= start_worktime:
                end_time = datetime.strptime('18:30', '%H:%M')
            end_time = end_time
        # 如果打卡时间在12:00和13:30之间
        elif start_time < lunch_end:
            end_time = lunch_end + timedelta(hours=7, minutes=30)
        else:
            # 如果打卡时间在13:30之后
            end_time = end_time - self.lunch_break_duration

        return end_time

    # 计算收益
    def calculate_earnings(self):
        start_time_str = self.input_starttime()
        start_worktime = datetime.strptime('09:30', '%H:%M').time()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        # 判断9:30之前打卡的工资也是按9:30算
        if start_time <= start_worktime:
            start_time = start_worktime
        else:
            start_time = start_time
        end_time = self.calculate_end_time(start_time_str).time()
        # 将日期和时间结合起来
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)
        while self.timer_active:
            now = datetime.now().time()
            now_datetime = datetime.combine(datetime.today(), now)
            # 计算今日工作时长，算上午休
            work_hours_today = (now_datetime - start_datetime).total_seconds() / 3600
            # 计算工时，不算上午休
            if start_time <= datetime.strptime('12:00', '%H:%M').time():
                work_hours = round(work_hours_today, 2)-1.5
            else:
                work_hours = round(work_hours_today, 2)
            # 计算今日收入
            earnings_today = work_hours_today * self.calculate_hourly_wage()
            # 计算距离下班还有多少秒
            with self.lock:
                if now_datetime < end_datetime:
                    off_work_time = (end_datetime - now_datetime).total_seconds()
                    print(f"\r当前收入：{earnings_today:.2f}元   工时：{work_hours:.2f}   距离下班时间：{off_work_time:.0f}秒", end='')
                    time.sleep(1)
                else:
                    print(f"已经下班了~  今日牛马费:{self.calculate_daily_wage():.2f}元")
                    break
        print("已退出程序")


if __name__ == '__main__':
    calculator = WorkdayCalculator()
    calculator.start()
    time.sleep(1)
    input("")
    calculator.stop()
