#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/10/13 09:16
# @Author : 新贵大人
描述:
"""
import requests
TOKEN = None

def init_token(token: str):
    global TOKEN
    TOKEN = token


def get_allocation_group_info():
    """获取分配组信息ID和班级ID列表"""
    allocation_group_info_ids = []
    class_ids = []

    url = "https://gw-mg-preprod.61info.cn/manager-api/o/new/allocate/group/getAllocationGroupList.json"
    params = {
        "level": 0,
        "allocationBatch": 4,
        "state": 0,
        "allocateGroupState": 0,
        "courseWeekDay": 0,
        "courseTimeScheduleId": 0,
        "startOpenCourseDate": "",
        "endOpenCourseDate": "",
        "batchOrder": "",
        "headTeacherStr": "",
        "keyword": "",
        "teacherId": 0,
        "queryTeacherId": "",
        "workGroupId": 0,
        "pageIndex": 4,
        "pageSize": 50,
        "allocationJoinState": 0,
        "userId": ""
    }

    headers = {
        "authorization": TOKEN,
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
        ).json()

        group_info_list = resp.get("data", {}).get("allocationGroupInfoList", [])
        for item in group_info_list:
            allocation_group_info_ids.append(item['allocationGroupInfoId'])
            group_info = item.get('groupInfo', {})
            class_id = group_info.get('classId', 0)
            if class_id != 0:
                class_ids.append(class_id)

    except Exception as e:
        print(f"获取分配组信息出错: {str(e)}")

    return allocation_group_info_ids, class_ids


def process_allocation_group(beginDate,endDate):
    url = "https://gw-mg-preprod.61info.cn/manager-api/o/new/allocate/group/getAllocationGroupUserList"
    allocation_group_info_ids, class_ids = get_allocation_group_info()
    for allocation_group_info_id, class_id in zip(allocation_group_info_ids, class_ids):
        data = {"pageNum": 1, "pageSize": 10, "allocationGroupId": allocation_group_info_id}
        header = {"authorization": TOKEN, 'content-type': 'application/json'}
        resp = requests.post(url, headers=header, json=data).json()
        if resp["data"]["list"] != []:
            for i in resp["data"]["list"]:
                dt = {"ignoreStopCourseTimes": "true",
                    "userId": i["userId"],
                    "beginDate": beginDate,
                    "endDate": endDate,
                    "stopReason": "测试特殊停课",
                    "stopType": "4",
                    "applyType": 1,
                    "cancelEnhanceCourse": "false",
                    "groupIds": [class_id]}
                url1 = "https://gw-mg-preprod.61info.cn/manager-api/o/apply/user/stop/course/newStopUserCourse.json"
                header = {"authorization": TOKEN, 'content-type': 'application/json;charset=UTF-8'}
                rq = requests.post(url1, headers=header, json=dt).json()
                print(f'处理学员: {i["userId"]}停课, 班级:{class_id} 执行结果: {rq["msg"]}')

if __name__ == '__main__':
    init_token("eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoicGgzMk4wK0diSThPZEhNMnZpbUJ5WDlKM2N2RXIxbFl0YVhZdmVxd1dENXV4bzJ0bCt2d0NkalJDTlBLR2lueG1yT2NiZlJuVys1eCttRnF3eTdBVFlIMEdWb0lEdk4vZGxLL3o1NXdvS0hJVFZJNHEwTUF4SEpLWkNISW1lUTNiY1dtUk9VSjlrMzZNOGpaVWV6SlFrMHhRT0d6OE5aNmFwTnpuYys4LzZBVGVoc2lXUVMybmlKVWVYWThNMDhMSDU5aXA2UWNjMVM4SUxNY2VDK2YzUnRGSjNsKzZ5eHNIVm9vY2pkNWNpeGloUkZBK0RVdEhnM0dWZDJrM2M3bXFBZ1h5Wld5TG4rUHRoZ0dYT1ZsaUJlRXp4Y1FQRDhFV1pWT2lZcTFHOW89IiwiZXhwIjoxNzc1OTUzMTU4fQ.XiPqLYAw8T8u4JI5_gSV9lV9leB85JD4m_ML8MB5CNs")
    process_allocation_group("2025-10-13", "2025-10-23")