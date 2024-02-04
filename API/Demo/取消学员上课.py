import requests

URL_LIST_STUDENT = "https://preprod-ems.vipthink.cn/gateway/route__jw/api/live_student/listStudent"
URL_CANCEL_LIVE = "https://preprod-ems.vipthink.cn/gateway/route__jw/work/live_student/cancel"

HEADERS = {
    "Origin": "https://preprod-crm.vipthink.cn",
    "Content-Type": "application/json;charset=UTF-8"
}


def cancel_live(lesson_id, Authorization):
    try:
        # 直播间详情
        live_detail = requests.get(URL_LIST_STUDENT, params={"lesson_id": lesson_id}, headers={
            "authorization": Authorization,
            **HEADERS
        }).json()
        if live_detail["code"] == 200:
            # 获取所有的未签到学员
            student_ids = [student['id'] for student in live_detail["data"] if student['checkStatus'] == 0]
            if not student_ids:
                return "没有可以取消的用户"
            for student in live_detail['data']:
                if student['studentId'] == 26601198:
                    for student_id in student_ids:
                        if student_id == student['id'] and student['checkStatus'] == 0:
                            # print("学员26601198，不做取消操作，后续有用例要用，状态是未签到")
                            continue
                        payload = {"liveStudentIds": [student_id], "reason": "课程详情 学员取消上课"}
                        requests.post(URL_CANCEL_LIVE, json=payload,
                                      headers={"authorization": Authorization, **HEADERS})
                        # print(student_id, "取消上课成功")
                    return 1
    except Exception as e:
        raise f"请求失败：{e}"


if __name__ == '__main__':
    print(cancel_live('9381134',
                'Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzA0MzQ5MDMxLCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3MDQ0MzU0MzEsImlhdCI6MTcwNDM0OTAzMSwic2lkIjoxfSx7InJhbmQiOiIxNDE2NTk2OTI0MTkxNzk2OTIzNjA3NDA0NTYyOTIzMjMwMzAxNTY1NTk0NzczMDYyODM4NTE5NTM0MDA5ODM4IiwidWlkIjo1MTM0NywidHlwIjoiYSIsInRpbWUiOjE3MDQzNDkwMzF9XQ.NjU2YWExZjcwZjkzN2YzN2VlMzkwNzBkZTFiOWVjMzBiM2ZiYjU2MGM2ZDUxM2M0NzdmMjhmOGY5N2E1MThiNw')
          )



