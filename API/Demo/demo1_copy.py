import requests,json,random


def get_moli_mobile(token):
    totalnum = 1
    while totalnum != 0:
        mobile = str("188") + str(random.randint(10000000, 99999999))
        url = "https://sht-eos-gateway.vipthink.cn/cc-backend/today/getUserList"
        data = {"nick_phone": mobile, "lru_flag": 1}
        header = {"Content-Type": "application/json",
                  "authorization": token}
        res = requests.post(url, data=json.dumps(data), headers=header)
        totalnum = json.loads(res.text)['data']['total']
    else:
        return mobile[0:11]

if __name__ == '__main__':
    print(get_moli_mobile('Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzIzMDg2NjAxLCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3MjMxNzMwMDEsImlhdCI6MTcyMzA4NjYwMSwic2lkIjoxfSx7InJhbmQiOiI5NjkzODgzOTUyNjEzNzYyODM4MzgyNDE1MTUwMjkwMjUxNTA2OTYzNTI0MzM2NjY1ODUyMzc1MjQyNjI4NzM3IiwidWlkIjo2Njc1MDgsInR5cCI6ImEiLCJ0aW1lIjoxNzIzMDg2NjAxfV0.Yjg2ZmM0NWE4YjU0NGVlZDM2MDA1ODJhMjg5YjI3NjNkMzkxNGFlMmU2MDRhYmJjOTIzNGYzZWE2NDBhYTg1NQ'
))