#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/08/14 17:07
# @Author : 新贵大人
描述:
"""


import pandas as pd
import requests
import json

def get_excel_data():
    df = pd.read_excel(r'C:\Users\92101\Desktop\导入结果1.xlsx')
    unique_df = df.drop_duplicates(subset=['班级id'])
    payloads = []
    for index, row in unique_df.iterrows():
        course_id = row['班级id']
        level_unit_lesson = row['lul'].split('-')
        level = int(level_unit_lesson[0])
        unit = int(level_unit_lesson[1])
        lesson = int(level_unit_lesson[2])
        try:
            next_teacher = json.loads(row['下一节课中外教老师'])
        except json.JSONDecodeError:
            print(f"班级 {course_id} 的 '下一节课中外教老师' 字段不是有效的 JSON 格式")
            continue
        previous_teacher_type = next_teacher['previousTeacherType']
        continuous_num = next_teacher['continuousNum']

        payload = {
            "courseId": course_id,
            "startTime": 1755532853000,  # 示例时间戳，根据需要调整
            "bookNum": 4,
            "level": level,
            "unit": unit,
            "lesson": lesson,
            "job": False,
            "operatorId": -1,
            "remoteIp": "127.0.0.1",
            "previousTeacherType": previous_teacher_type,
            "continuousNum": continuous_num
        }
        payloads.append(payload)
    return payloads


def post():
    url = "http://apistaging.mmears.com/course-service/api/cambridge/course/bookCourseByCourseIdAndStartTime"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": "123456"
    }
    for payload in get_excel_data():
        course_id = payload['courseId']
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"班级 {course_id}: {response.status_code}, {response.json()}")

if __name__ == '__main__':
    post()