import requests


def get_quanxian():
    url = "https://uat-iam-staff-admin.vipthink.cn/iam-admin/v1/user/getDetail"
    payload = {
        "adminId": 4968,
        "unitCode": 6666
    }
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNjgwNTkzMjY3LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE2ODA2Nzk2NjcsImlhdCI6MTY4MDU5MzI2Nywic2lkIjoxfSx7InJhbmQiOiIyMjUyNTkxNTUwODQxNTk1ODExNjg1NzgzMTM0MTE0Mzk3MDE3NjkxNTMyMTQxMTcyNzE3NjMxMTM0MTQ2NzY3IiwidWlkIjo0OTY4LCJ0eXAiOiJhIiwidGltZSI6MTY4MDU5MzI2N31d.NDY0NmUyODJjNDNkMzI2ZTUwYjVjNjk3NTVjZGE1YjVlZDJlNjJiZWY3ZWNhZDA2OTE0OTgzNmFmZTM1MzQ0Zg",
        "origin": "https://uat-iam-staff.vipthink.cn",
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    liebiao = []
    for i in response.json()['data']['roleList']:
        liebiao.append(i['id'])
    return liebiao


if __name__ == '__main__':
    url1 = "https://uat-iam-staff-admin.vipthink.cn/iam-admin/v1/user/edit"
    payload1 = {
        "roleIdList": get_quanxian(),
        "isTest": "0",
        "adminId": 666990
    }
    headers1 = {
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNjgwNTkzMjY3LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE2ODA2Nzk2NjcsImlhdCI6MTY4MDU5MzI2Nywic2lkIjoxfSx7InJhbmQiOiIyMjUyNTkxNTUwODQxNTk1ODExNjg1NzgzMTM0MTE0Mzk3MDE3NjkxNTMyMTQxMTcyNzE3NjMxMTM0MTQ2NzY3IiwidWlkIjo0OTY4LCJ0eXAiOiJhIiwidGltZSI6MTY4MDU5MzI2N31d.NDY0NmUyODJjNDNkMzI2ZTUwYjVjNjk3NTVjZGE1YjVlZDJlNjJiZWY3ZWNhZDA2OTE0OTgzNmFmZTM1MzQ0Zg",
        "origin": "https://uat-iam-staff.vipthink.cn",
    }
    response = requests.request("POST", url1, json=payload1, headers=headers1)
    print(response.text)
