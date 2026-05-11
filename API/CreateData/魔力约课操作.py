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


def get_excel_data(file_path, startTime):
    df = pd.read_excel(file_path)
    unique_df = df.drop_duplicates(subset=['班级id']).sort_values(by='班级id', ascending=True)
    payloads = []
    for index, row in unique_df.iterrows():
        course_id = int(row['班级id'])
        level_unit_lesson = row['lul'].split('-')
        level = int(level_unit_lesson[0])
        unit = int(level_unit_lesson[1])
        lesson = int(level_unit_lesson[2])
        try:
            next_teacher = json.loads(row['下一节课中外教老师'])
        except json.JSONDecodeError:
            corrected_str = "{" + row['下一节课中外教老师'] + "}"
            try:
                next_teacher = json.loads(corrected_str)
            except json.JSONDecodeError as e:
                print(f"班级 {course_id} 的'下一节课中外教老师'字段无法修正为有效的json格式: {e}")
                continue
        previous_teacher_type = next_teacher['previousTeacherType']
        continuous_num = next_teacher['continuousNum']

        payload = {
            "courseId": course_id,
            "startTime": startTime,
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


def post_book_course(url, token, payloads, output_path):
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    # for payload in payloads:
    #     course_id = payload['courseId']
    #     try:
    #         response = requests.post(url, headers=headers, data=json.dumps(payload))
    #         print(f"班级 {course_id}: {response.status_code}, {response.json()}")
    #     except requests.exceptions.RequestException as e:
    #         print(f"请求失败，班级 {course_id}: {e}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for payload in payloads:
            course_id = payload['courseId']
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                result = f"班级 {course_id}: {response.status_code}, {response.json()}"
                print(result)
                f.write(result + '\n')
            except requests.exceptions.RequestException as e:
                error_msg = f"请求失败，班级 {course_id}: {e}"
                print(error_msg)
                f.write(error_msg + '\n')


# if __name__ == '__main__':
#     file_path = r'C:\Users\92101\Desktop\第五批导入结果.xlsx'
#     startTime = "1758556800000"
#     url = "https://api.mmears.com/course-service/api/cambridge/course/bookCourseByCourseIdAndStartTime"
#     token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI1NiIsIm5hbWUiOiLosK3mlrDotLUiLCJzdXBwb3J0SWQiOm51bGwsImV4cCI6MTc1ODE3ODI1NiwiaWF0IjoxNzU4MDkxODU2LCJlbWFpbCI6InRhbnhpbmd1aUBobHRuLmNvbSJ9.GDWZ-JaFrw8m01ChjXF32--WkmYCMlvUaB_Wb3bqy0y8IVO9VPNTWwKfzIon4IOuGxwmF2po4f774b_aNnpiyQ"
#     payloads = get_excel_data(file_path, startTime)
#     post_book_course(url, token, payloads)

if __name__ == '__main__':
    file_path = r'C:\Users\92101\Desktop\第五批没外教数据.xlsx'
    startTime = "1758556800000"
    url = "https://api.mmears.com/course-service/api/cambridge/course/bookCourseByCourseIdAndStartTime"
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI1NiIsIm5hbWUiOiLosK3mlrDotLUiLCJzdXBwb3J0SWQiOm51bGwsImV4cCI6MTc1ODU5NTAxMiwiaWF0IjoxNzU4NTA4NjEyLCJlbWFpbCI6InRhbnhpbmd1aUBobHRuLmNvbSJ9.HmZC31YT6WJeh9psSurJJDIpA2rUz-wIvbTElycAMJF1-pNH1MHkGTDtHZt2184WXloK5AixgQcLedRPKCjQRA"
    output_path = r'C:\Users\92101\Desktop\约课结果.txt'
    payloads = get_excel_data(file_path, startTime)
    post_book_course(url, token, payloads, output_path)
