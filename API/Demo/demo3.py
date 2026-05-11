# import datetime
# def today_date():
#     today = datetime.datetime.now().date()
#     return today
#
# def future_num_date(num_day):
#     future_date = today_date() + datetime.timedelta(days=num_day)
#     return str(future_date)


import json
import random
import requests
import time


def get_moli_mobile(token):
    while True:
        mobile = str("187") + str(random.randint(10000000, 99999999))
        url = "https://sht-eos-gateway.vipthink.cn/cc-backend/today/getUserList"
        data = {"nick_phone": mobile, "lru_flag": 1}
        header = {"Content-Type": "application/json",
                  "authorization": token}
        res = requests.post(url, data=json.dumps(data), headers=header)
        if res.status_code == 200 and json.loads(res.text)['data']['total'] == 0:
            return mobile[0:11]

def add_fixed_teacher_banci(token,combinationIds,teacherId):
    url = "https://apistaging.mmears.com/teacher/fixed/class/edit/relation"
    data = {'combinationIds': [combinationIds], 'teacherId': teacherId}
    header = {"X-Auth-Token": token, "X-App-Id": "6"}
    while True:
        try:
            response = requests.post(url, json=data, headers=header).json()
            if response["code"] == "OK":
                return 1
            elif response["code"] == "BIZ_FAIL":
                time.sleep(5)  # 等待5秒后继续调用该接口
            else:
                raise Exception("接口执行错误，并非排课中")
        except Exception as e:
            print("Error: ", e)
            time.sleep(5)  # 等待5秒后重试

if __name__ == '__main__':
    print(add_fixed_teacher_banci("eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI1NiIsIm5hbWUiOiLosK3mlrDotLUiLCJzdXBwb3J0SWQiOm51bGwsImV4cCI6MTcwNTcyMjc2MCwiaWF0IjoxNzA1NjM2MzYwLCJlbWFpbCI6InRhbnhpbmd1aUBobHRuLmNvbSJ9.cB7MKR0d0307LReX83r8PtoUFFloJzerKsrMWkf-FBjw-WwH8nR2Gp1J0wY597LN8t78oxnr-CkrMdpt1K96EQ","13","594601"))