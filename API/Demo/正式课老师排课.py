#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/01/06 16:24
# @Author : 新贵大人
描述:
"""

import base64
import requests
from concurrent.futures import ThreadPoolExecutor


class ArrangeCourse:
    def uat_login(self, environment, username=18707699952, passw='klzz1234@@'):
        url = f'https://{environment}-auth-new.vipthink.cn/iam-sso/v2/auth/admin/token'
        data = {
            "account": username,
            "password": base64.b64encode(passw.encode()).decode('utf-8'),
            "loginType": "acc_pwd"
        }
        reps = requests.post(url, json=data)
        return reps.json()['data']['token']

    def reset_teacher_time(self, teacherId, calId, hours, catSids, environment):
        # 测试环境：120分钟方案
        # time_strings = ["08:00", "10:10", "12:20", "14:30", "16:40", "18:50", "21:00", "23:10"]
        # uat专用方案
        global time_data
        uat_time_strings = [
            "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00", "15:00", "16:00", "16:50", "17:40", "18:30", "19:20", "20:10", "21:00",
            "22:00", "22:50", "23:40"]

        preprod_time_strings = [
            "00:00", "01:00", "06:00", "07:00", "08:00", "09:00","10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
            "16:00", "16:50", "17:40", "18:30", "19:20", "20:10","21:00", "22:00", "23:00"]

        url = f"https://{environment}-tqs.vipthink.cn/api/edu_teach/resetTeacherTime"
        headers = {"authorization": self.uat_login(environment)}

        if environment == "uat":
            time_data = [(int(t.split(':')[0]), int(t.split(':')[1])) for t in uat_time_strings]
        elif environment == "preprod":
            time_data = [(int(t.split(':')[0]), int(t.split(':')[1])) for t in preprod_time_strings]

        def send_request(time_tuple, week_day):
            hour, minute = time_tuple
            data = {
                "teacherId": teacherId,
                "calId": calId,
                "timeBean": {
                    "week": week_day,
                    "hour": hour,
                    "minute": minute,
                    "hours": hours,
                    "catSids": catSids
                }
            }
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                return response.json()
            except requests.RequestException as e:
                return {"error": str(e)}

        # 线程池并发发送请求
        with ThreadPoolExecutor(max_workers=20) as executor:
            rsps = []
            for hour, minute in time_data:
                for week_day in range(1, 8):
                    rsps.append(executor.submit(send_request, (hour, minute), week_day))

            for rsp in rsps:
                result = rsp.result()
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print("排班结束")


if __name__ == "__main__":
    arrange_course = ArrangeCourse()
    # arrange_course.reset_teacher_time(
    #     #测试环境老师：圆圆老师01：1081  小桥老师：900   瑶瑶老师：148   关关老师：487  白菜老师：596  叶梅：220
    #     teacherId="220",
    #     calId="27",
    #     hours=40,
    #     catSids=[5310],
    #     environment='test'
    # )

    arrange_course.reset_teacher_time(
        #预发布环境  羊羊老师：47
        teacherId="667508",
        calId="27",
        hours=40,
        catSids=[5858],
        environment='uat'
    )
