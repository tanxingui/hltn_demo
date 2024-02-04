#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/12/27 11:23
# @Author : 新贵大人
描述:测试环境排班
"""
import base64
import time
import requests


def get_base64(passwd):
    b_pwd = base64.b64encode(passwd.encode()).decode('utf-8')
    return b_pwd


def uat_login(username=15979225192, passw='jnniey0924@'):
    url = 'https://uat-auth-new.vipthink.cn/iam-sso/v2/auth/admin/token'
    data = {
        "account": username,
        "password": get_base64(passw),
        "loginType": "acc_pwd"
    }
    reps = requests.post(url, json=data)
    return reps.json()['data']['token']


def add_ceshiclass():
    Day_1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    Day_2 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 1 * 24 * 60 * 60))
    Day_3 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 2 * 24 * 60 * 60))
    Day_4 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 3 * 24 * 60 * 60))
    Day_5 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 4 * 24 * 60 * 60))
    Day_6 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 5 * 24 * 60 * 60))
    Day_7 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 6 * 24 * 60 * 60))

    data = {
        "teachArr": [113, 312, 399, 545, 821, 900, 1411, 1432, 1611],
        "dateArr": [Day_1, Day_2, Day_3, Day_4, Day_5, Day_6, Day_7],
        "planId": 88,
        # 测试环境uat专用班次方案
        "hourArr":
            ["01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
             "12:00", "13:00", "14:00", "15:00", "16:00", "16:50", "17:40", "18:30", "19:20", "2010", "21:00",
             "22:00", "22:50", "23:40"],
        "type": 1,
        "maxClassNum": 6,
        "classHour": 40,
        "hourConsume": 0,
        # 新增排课的上课阶段stepId
        "cateIdArr": [6272],

    }
    url = "https://uat-tqs.vipthink.cn/api/edu_plan/batchReplenish"
    headers = {"authorization": f"{uat_login()}"}
    resp = requests.post(url=url, headers=headers, json=data)
    return resp.json()  # 排班成功返回{'msg': 'SUCC', 'code': 200}


if __name__ == '__main__':
    print(uat_login())
