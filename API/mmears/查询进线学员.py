#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/01/03 16:18
# @Author : 新贵大人
描述:循环查看进线学员(clp魔力)
"""
import time
import requests

def get_mmears_student_id(host, phone, token) -> str:
    url = f"{host}/eos-lp/common/searchUser"
    body = {"keywords": phone}
    headers = {"Authorization": token}
    for i in range(2):
        try:
            resp = requests.post(url, json=body, headers=headers, timeout=5).json()
            if resp.get("code") == 0:
                users = resp.get("data", {}).get("users", [])
                if users:
                    return users[0]["id"]
            time.sleep(5)
        except requests.exceptions.RequestException:
            # 出现异常则暂停10秒
            print(f"请求异常，等待10秒后重试，已重试{i+1}次")
            time.sleep(3)
    return "查询不到学员id"

if __name__ == '__main__':
    print(get_mmears_student_id('https://sht-eos-gateway.vipthink.cn', "13824253468",
                               "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzA0MjcwNzY1LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3MDQzNTcxNjUsImlhdCI6MTcwNDI3MDc2NSwic2lkIjoxfSx7InJhbmQiOiI5MDcyNDQ1ODAwMzk1NTQwNDUyNzg3NDI1MDc3NDU0NDE0ODUwODk1NTg0MTc2OTY0NzI0NDYwMTg1OTQ5NDY4IiwidWlkIjo0OTY4LCJ0eXAiOiJhIiwidGltZSI6MTcwNDI3MDc2NX1d.NjViMWVkZmI0NzgyN2U5ZDE4ZjQxMzNiOTFmZDUyODZiMjk5Yjg3ZjdhNjlhMDA1ZmNlNGJlNjIxNjhkMmJiNg"))
