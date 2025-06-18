import requests


token = "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzQ5NjExMTg4LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3NDk2OTc1ODgsImlhdCI6MTc0OTYxMTE4OCwic2lkIjoxfSx7InJhbmQiOiI0Mjk1NzAyMTc1OTA3NDI2ODU3MDA5MDc3Mjc5MjMxMTA3MDM0MDQ3NjgzNzQ4MTAzMzEzNjA0ODk2MDk5MzU3IiwidWlkIjo2NjcwMTYsInR5cCI6ImEiLCJ0aW1lIjoxNzQ5NjExMTg4fV0.MDJjMmJiNjUxMzQzMTgxOTUxYTNlMzMxZjUzODNhOTEwNzU4MDViOWQyYTNlZTdhOTRhYTkwNzY4M2NlMjM2Yw"
origin = "https://uat-iam-staff-admin.vipthink.cn"

def get_quanxian():
    url = f"{origin}/iam-admin/v1/user/getDetail"
    payload = {
        "adminId": 531,
        "unitCode": 6666
    }
    headers = {
        "content-type": "application/json",
        "authorization": token,
        "origin": origin,
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    liebiao = []
    for i in response.json()['data']['roleList']:
        liebiao.append(i['id'])
    return liebiao


if __name__ == '__main__':
    url1 = f"{origin}/iam-admin/v1/user/edit"
    payload1 = {
        "roleIdList": get_quanxian(),
        "isTest": "1",
        "adminId": 667508
    }
    headers1 = {
        "content-type": "application/json",
        "authorization": token,
        "origin": origin,
    }
    response = requests.request("POST", url1, json=payload1, headers=headers1)
    print(response.text)
