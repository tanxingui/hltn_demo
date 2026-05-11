#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/03/10 16:53
# @Author : 新贵大人
描述:
"""
import requests


def cancel_old_student_click(Authorization):
    URL_OldAllocatedUserList = "https://gw-mg-preprod.61info.cn/manager-api/o/allocate/old/getOldAllocatedUserList"
    all_data = []
    page = 1
    size = 50
    while True:
        data = {
            "beginCourseStageId": "",
            "week": "",
            "courseTimeId": "",
            "applyState": 2,
            "batchOrder": "",
            "headTeacherId": "",
            "csId": "",
            "page": page,
            "size": size,
            "keyword": "",
            "workGroupId": "",
            "courseTableId": ""
        }

        resp = requests.post(URL_OldAllocatedUserList, json=data, headers={"authorization": Authorization})
        resp_json = resp.json()

        if resp.status_code != 200 or resp_json.get('code') != 0:
            print(f"请求失败, 状态码: {resp.status_code}, 响应数据: {resp_json}")
            break

        total = resp_json['data']['total']
        user_list = resp_json['data']['list']

        if not user_list:
            break

        for user in user_list:
            begin_course_stage_id = user.get('beginCourseStageId')
            user_id = user.get('userId')
            course_table_id = user.get('courseTableId')
            if begin_course_stage_id is not None and user_id is not None and course_table_id is not None:
                all_data.append(
                    {'beginCourseStageId': begin_course_stage_id, 'userId': user_id, 'courseTableId': course_table_id})

        if len(all_data) >= total:
            break
        page += 1

    # 调用下一个接口
    url_cancelOldChoice = "https://gw-mg-preprod.61info.cn/manager-api/o//allocate/old/cancelOldChoice"
    for item in all_data:
        next_data = {
            "beginCourseStageId": item['beginCourseStageId'],
            "userId": item['userId'],
            "courseTableId": item['courseTableId']
        }
        response = requests.get(url_cancelOldChoice, params=next_data, headers={"authorization": Authorization})
        if response.json()["code"] == 0:
            print(f"取消老生学员：{item['userId']}已选分班成功")
        else:
            print(f"取消失败，学员id：{item['userId']}")


if __name__ == '__main__':
    cancel_old_student_click(
        'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoicGgzMk4wK0diSThPZEhNMnZpbUJ5WDlKM2N2RXIxbFl0YVhZdmVxd1dENXV4bzJ0bCt2d0NkalJDTlBLR2lueG1yT2NiZlJuVys1eCttRnF3eTdBVFlIMEdWb0lEdk4vZGxLL3o1NXdvS0hJVFZJNHEwTUF4SEpLWkNISW1lUTNiY1dtUk9VSjlrMzZNOGpaVWV6SlFrMHhRT0d6OE5aNmFwTnpuYys4LzZDR1phN05wUmhWUUdHRVJoSGlvSUJlR1ZzYTRnOVFKNDJNNzhjR1JqQ1lncWhIcmF2VUc4UFd6b3hsSnJUUEpVdys3aDZmKy9CNHVVdjlEekpVM1Ezd05FWWhXZ3AzQ1RvQzBUM0YySHVTeVU2cDdRSGRNREdRNVZkQ0swcDY2RnJON0RDeDdMZmZMTHRJNEdubm5wR04iLCJleHAiOjE3ODQ1MzM5NDJ9.9__tu6m5Mzpkb3nxrYLdhXD_7FVb1mq4_I82MaZgaik')
