#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/06/28 18:11
# @Author : 新贵大人
描述:
"""
import base64

import requests


class UserInputHandler:
    def __init__(self):
        self.subject = self.get_subject()
        self.environment = self.get_environment()
        self.custom_number = self.get_custom_phone_number()
        if self.custom_number == "0":
            self.num = self.get_num()

    @staticmethod
    def get_base64(string):
        encoded = base64.b64encode(string.encode('utf-8'))
        return encoded.decode('utf-8')

    def get_crm_login_token(self, username, passw):
        url = f'https://{self.environment}-auth-new.vipthink.cn/iam-sso/v2/auth/admin/token'
        data = {
            "account": username,
            "password": self.get_base64(passw),
            "loginType": "acc_pwd"
        }
        resp = requests.post(url, json=data).json()
        if resp['code'] == 0:
            token = resp.get('data', {}).get('token', '')
            return token
        else:
            print("登录出错")

    def get_subject(self):
        while True:
            subject = input("请输入：(1)-->口才    (2)-->益智    (3)-->魔力")
            try:
                subject = int(subject)
            except ValueError:
                print("输入错误，请输入数字")
                continue
            if subject == 1:
                return "口才"
            elif subject == 2:
                return "益智"
            elif subject == 3:
                return "魔力"
            else:
                print("请输入一个数字(1)/(2)获取正确的学科")

    def get_environment(self):
        while True:
            environment = input("请输入：(1)-->测试环境    (2)-->预发布环境")
            try:
                environment = int(environment)
            except ValueError:
                print("输入错误，请输入数字")
                continue
            if environment == 1:
                return "uat"
            elif environment == 2:
                return "preprod"
            else:
                print("请输入一个数字(1)/(2)获取正确的环境")

    def get_custom_phone_number(self):
        while True:
            custom_number = input("请输入你需要导单的手机号(用逗号隔开)，输入0则不需要自定义:-->")
            try:
                if custom_number == "0":
                    return custom_number
                elif custom_number == "":
                    return str(0)
                else:
                    custom_number = custom_number.replace('，', ',').replace('、', ',').replace('.', ',').replace('。', ',').replace(' ', ',')
                    phone_numbers = custom_number.split(',')
                    for phone_number in phone_numbers:
                        phone_number = phone_number.strip()
                        if len(phone_number) != 11:
                            print("请输入11位数字的手机号")
                            break
                    else:
                        return phone_numbers
            except ValueError:
                print("输入错误，请输入数字")

    def get_num(self):
        while True:
            num = input(f"请输入{self.environment}环境需要导入的订单条数:")
            try:
                num = int(num)
            except ValueError:
                print("输入错误，请输入数字")
                continue
            if 0 < num <= 100:
                return num
            else:
                print("请输入大于0，小于100的数字")

