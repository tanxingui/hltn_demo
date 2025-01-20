# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# # @Time   : 2025/01/06 16:24
# # @Author : 新贵大人
# 描述:
# """
# import base64
# import requests
#
#
# def uat_login(username=19191919191, passw='a@123456789'):
#     url = 'https://uat-auth-new.vipthink.cn/iam-sso/v2/auth/admin/token'
#     data = {
#         "account": username,
#         "password": base64.b64encode(passw.encode()).decode('utf-8'),
#         "loginType": "acc_pwd"
#     }
#     reps = requests.post(url, json=data)
#     return reps.json()['data']['token']
#
# def reset_teacher_time(teacherId,calId,duration,catSids):
#     # 120分钟方案
#     # time_strings = ["08:00", "10:10", "12:20", "14:30", "16:40", "18:50", "21:00", "23:10"]
#     # uat专用方案
#     time_strings = ["01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
#              "12:00", "13:00", "14:00", "15:00", "16:00", "16:50", "17:40", "18:30", "19:20", "2010", "21:00",
#              "22:00", "22:50", "23:40"]
#
#     for time_str in time_strings:
#         hour, minute = map(int, time_str.split(':'))
#         for i in range(7):
#             url = 'https://uat-tqs.vipthink.cn/api/edu_teach/resetTeacherTime'
#             data = {"teacherId": teacherId, "calId": calId, "timeBean": {"week": i+1, "hour": hour, "minute": minute, "duration": duration, "catSids": catSids}}
#             headers = {"authorization": f"{uat_login()}"}
#             reps = requests.post(url, headers=headers, json=data)
#             print(reps.json())
#
#
# if __name__ == '__main__':
#     reset_teacher_time(1081, 27, 40, [5310])  # 圆圆老师01
import base64
import requests
from concurrent.futures import ThreadPoolExecutor

def uat_login(username=19191919191, passw='a@123456789'):
    url = 'https://uat-auth-new.vipthink.cn/iam-sso/v2/auth/admin/token'
    data = {
        "account": username,
        "password": base64.b64encode(passw.encode()).decode('utf-8'),
        "loginType": "acc_pwd"
    }
    reps = requests.post(url, json=data)
    return reps.json()['data']['token']

def reset_teacher_time(teacherId, calId, duration, catSids):
    # 120分钟方案
    # time_strings = ["08:00", "10:10", "12:20", "14:30", "16:40", "18:50", "21:00", "23:10"]
    # uat专用方案
    time_strings = [
        "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00", "16:00", "16:50", "17:40", "18:30", "19:20", "20:10", "21:00",
        "22:00", "22:50", "23:40"]

    url = "https://uat-tqs.vipthink.cn/api/edu_teach/resetTeacherTime"
    headers = {"authorization": uat_login()}

    # 提前解析时间字符串
    time_data = [(int(t.split(':')[0]), int(t.split(':')[1])) for t in time_strings]

    # 定义请求发送函数
    def send_request(time_tuple, week_day):
        hour, minute = time_tuple
        data = {
            "teacherId": teacherId,
            "calId": calId,
            "timeBean": {
                "week": week_day,
                "hour": hour,
                "minute": minute,
                "duration": duration,
                "catSids": catSids
            }
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # 使用线程池并发发送请求
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for hour, minute in time_data:
            for week_day in range(1, 8):  # 1到8表示周一到周日
                futures.append(executor.submit(send_request, (hour, minute), week_day))

        # 收集并打印结果
        for future in futures:
            result = future.result()
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print("排课完成")

# 示例调用
if __name__ == "__main__":
    # 圆圆老师01 id：1081    关关老师：487
    reset_teacher_time(
        teacherId="1081",
        calId="27",
        duration=40,
        catSids=[5310]
    )
