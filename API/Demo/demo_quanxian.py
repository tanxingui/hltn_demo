import requests


token = "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNjkwNzkyMTM3LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE2OTA4Nzg1MzcsImlhdCI6MTY5MDc5MjEzNywic2lkIjoxfSx7InJhbmQiOiIyNzQxMTgwNDc3NjkyNTUyNjU0MDc1OTkzNTE5NTA2NjQ1NDUxOTUzMTIxMzgzMzIyNzYzMzgwODEyNTI4MDA3IiwidWlkIjo1MTM0NywidHlwIjoiYSIsInRpbWUiOjE2OTA3OTIxMzd9XQ.YmIzNjZhZTljMGVhMTllODkwMTAxY2U0YjRjZjU2YWM2Mjc4YWQxNWRhNWE3MWI2ODQ4MGFjYjBhMjVmOTBiOA"
origin = "https://preprod-iam-staff.vipthink.cn"

def get_quanxian():
    url = "https://preprod-iam-staff-admin.vipthink.cn/iam-admin/v1/user/getDetail"
    payload = {
        "adminId": 50714,
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
    url1 = "https://preprod-iam-staff-admin.vipthink.cn/iam-admin/v1/user/edit"
    payload1 = {
        "roleIdList": get_quanxian(),
        "isTest": "1",
        "adminId": 51347
    }
    headers1 = {
        "content-type": "application/json",
        "authorization": token,
        "origin": origin,
    }
    response = requests.request("POST", url1, json=payload1, headers=headers1)
    print(response.text)
