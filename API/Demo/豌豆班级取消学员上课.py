import requests

URL_LIST_STUDENT = "https://preprod-ems.vipthink.cn/gateway/route__jw/api/live_student/listStudent"
URL_CANCEL_LIVE = "https://preprod-ems.vipthink.cn/gateway/route__jw/work/live_student/cancel"

HEADERS = {
    "Origin": "https://preprod-crm.vipthink.cn",
    "Content-Type": "application/json;charset=UTF-8"
}

def cancel_live(lesson_id, Authorization):
    try:
        all_students = []
        for page_num in range(1, 200):
            params = {
                "lesson_id": lesson_id,
                "page_num": page_num,
                "page_size": 100
            }
            response = requests.get(
                URL_LIST_STUDENT,
                params=params,
                headers={"authorization": Authorization, **HEADERS}
            )
            if response.status_code == 200:
                data = response.json()
                if data["code"] == 200:
                    students = data["data"]["list"]
                    if not students:
                        break
                    all_students.extend(students)
                else:
                    print(f"获取学生列表失败：{data.get('msg', '未知错误')}")
                    break
            else:
                print(f"获取学生列表请求失败，状态码：{response.status_code}")
                break

        uncheck_students = [student for student in all_students if
                            student['checkStatus'] == 0 and student['studentId'] != 26601198]

        if not uncheck_students:
            return 2

        # 取消未签到学员的上课
        for student in uncheck_students:
            payload = {
                "liveStudentIds": [student['id']],
                "reason": "课程详情 学员取消上课"
            }
            response = requests.post(
                URL_CANCEL_LIVE,
                json=payload,
                headers={"authorization": Authorization, **HEADERS}
            )
            if response.status_code == 200:
                data = response.json()
                if data["code"] == 200:
                    print(f"学员{student['studentId']}取消上课成功")
                else:
                    print(f"学员{student['studentId']}取消上课失败：{data.get('msg', '未知错误')}")
            else:
                print(f"学员{student['studentId']}取消上课失败：请求失败，状态码：{response.status_code}")

        return 1

    except Exception as e:
        print(f"取消直播操作失败：{e}")
        return f"请求失败：{e}"
if __name__ == '__main__':
    print(cancel_live('9408453',
                'Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzcyMDA2MTY1LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3NzIwOTI1NjUsImlhdCI6MTc3MjAwNjE2NSwic2lkIjoxfSx7InJhbmQiOiI3NTIxMDE4NDcxNzI3NDk4NTQyNjM0MDYwMTgzMTMwOTc1NzI1OTM2OTQ5NjI1MTA0MjMxMTYyNTUwNjUxNzY5IiwidWlkIjo1MTM0NywidHlwIjoiYSIsInRpbWUiOjE3NzIwMDYxNjV9XQ.ZGIwN2U1MWQ5OWU2OTdiMDliZGY5OWIwM2Y3YTBjNjc5MDhkMjJjNGUzNzNkODJhMzZhY2MzYzI3MGYwMGNjYg'))