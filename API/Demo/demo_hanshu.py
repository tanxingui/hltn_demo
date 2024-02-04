#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/05/10 20:54
# @Author  : 新贵大人

import json
from datetime import datetime, timedelta
import re
import time
import jsonpath
import requests
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA


# ecc获取token
def get_clpkoucai_token(username, pwd):
    url = 'https://preprod-auth.vipthink.cn/v1/auth/admin/token'
    data = {"__fields": "token,uid", "username": username, "password": pwd}
    token = requests.post(url, json=data).json()['data']['token']
    uid = requests.post(url, json=data).json()['data']['uid']
    url_koucai = 'https://preprod-eos-gateway.vipthink.cn/cc-backend/public/business/setBusinessId'
    data_koucai = {"token": token, "admin_id": uid, "biz_id": 5}
    header_koucai = {"authorization": token, "content-type": 'application/json'}
    requests.post(url=url_koucai, data=json.dumps(data_koucai), headers=header_koucai)
    return token


# 获取ecc跟老用户不重复的手机号，中间是时间戳
def get_phone1(host, token):
    try:
        while True:
            now = time.time()
            new_phone = '1' + str(int(now))
            url = f"{host}/cc-backend/today/getUserList"
            data = {"nick_phone": new_phone, "lru_flag": 1}
            header = {"authorization": token}
            # 请求查询学员接口
            res = requests.post(url, json=data, headers=header)
            print(res.json())
            if jsonpath.jsonpath(res.json(), '$.data.total')[0] == 0:
                return new_phone
            else:
                continue
    except TypeError as error:
        print('接口请求异常，请检查token\n', 'error:', error)


# 获取clp跟老用户不重复的手机号，中间是时间戳
def get_phone2(host, token):
    try:
        while True:
            now = time.time()
            new_phone = '1' + str(int(now))
            url = f"{host}/eos-lp/common/searchUser"
            data = {"keywords": new_phone}
            header = {"authorization": token}
            # 请求查询学员接口
            res = requests.post(url, json=data, headers=header)
            if jsonpath.jsonpath(res.json(), '$.data.users')[0] == []:
                return new_phone
            else:
                continue
    except TypeError as error:
        print('接口请求异常，请检查token\n', 'error:', error)


# 豌豆侧用户中心rsa 公钥
WANDOU_PUBLIC_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCw1znRd8ck4JujUxBvQKBYGykn1kLafsyNVw4hN+LN93PiFwLiQgfzDZewTuqhWhjegVbcKgAf8MCsYHSZ9FdKRueVZwqM4nRQ+HuL9tolp7JIv7S9CLt7zvkxZW7xIN92JPs+rppBIVIwLNkwBxy1M5KgQClwhGK5eHAsB4AfhwIDAQAB"


def get_wandow_encrypt(phone_pwd):
    # 获取豌豆侧用户中心，手机号或密码加密后的密文
    wpk_public_key = '-----BEGIN PUBLIC KEY-----\n' + WANDOU_PUBLIC_KEY + '\n-----END PUBLIC KEY-----'
    rsa_key = RSA.importKey(wpk_public_key)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    encrypt_text = cipher.encrypt(phone_pwd.encode())
    cipher_text_tmp = base64.b64encode(encrypt_text)
    return cipher_text_tmp.decode()


# 进线
def jinxian():
    url = 'https://preprod-gw.vipthink.cn/api/memberaggr/unau/user/verificationLogin'
    data = {
        "areaCode": 86,
        "phoneCipher": get_wandow_encrypt('18707600004'),
        "cipherVersion": "v1",
        "verificationCodeToken": "default",
        "appTypeCode": "MASTER_WECHAT",
        "ext": "{\"mid\":\"278926\",\"url\":\"https://preprod-h4.vipthink.cn/pre/merak/1713.html?mid=278926&appTypeCode=&drawlalaUserId=&drawlalaPhone=&dialogClose=true\",\"type\":\"merak\",\"skuId\":\"10002218\",\"grayCode\":\"mkdMerak\",\"channelId\":470630}",
        "registered": "true",
        "verificationCode": "7311",
        "source": 470630
    }
    res = requests.post(url=url, json=data,
                        headers={"authorization": get_clpkoucai_token('17621389856', 'Klzz1234'), "appid": '46620459'})
    print(res.json())


# 获取url的值
def get_url_value(url, str1, str2):
    value = re.findall(str1 + "(.*?)" + str2, url)[0]
    return value

# 获取当前时间以及xx时间后的时间(年月日)
def get_date_and_next_days(num):
    current_date = datetime.now()
    next_days = current_date + timedelta(days=num)
    current_date_str = current_date.strftime('%Y-%m-%d')
    next_days_str = next_days.strftime('%Y-%m-%d')
    return [current_date_str, next_days_str]

def today_date():
    today = datetime.now().date()
    return today

def future_num_date(num_day):
    future_date = today_date() + timedelta(days=num_day)
    return future_date

if __name__ == '__main__':
    print(future_num_date(10))
