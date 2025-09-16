#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/09/16 19:00
# @Author : 新贵大人
描述:
"""
import pandas as pd
import re
import pymysql
import requests
from collections import defaultdict

mysql_moli_test = pymysql.connect(host='172.23.59.64', port=3306, user='mmtest', password='Mmears2023',
                                       db='db_course')
def get_csv():
    df = pd.read_csv(r'C:\Users\92101\Desktop\mmears-prod-bj_titan-mmears-course-service_20250916_183539.csv')
    results = []
    # 正则
    class_info_pattern = re.compile(r'classInfo:(\d+)')
    start_time_pattern = re.compile(r'startTime:(\d+)')
    dto_pattern = re.compile(r'StudentBookResultDTO\([^)]+\)')

    # 遍历
    for _, row in df.iterrows():
        message = row['message']
        if pd.isna(message):
            continue

        class_info = int(class_info_pattern.search(message).group(1))
        start_time = int(start_time_pattern.search(message).group(1))

        # 提取每个DTO块
        for dto in dto_pattern.findall(message):
            if 'bookCode=10' in dto and 'bookResult=学生课时不足' in dto:
                student_id = int(re.search(r'studentId=(\d+)', dto).group(1))
                results.append({
                    'classInfo': class_info,
                    'startTime': start_time,
                    'studentId': student_id
                })
    return results

def get_db_information(class_info, start_time):
    cursor = mysql_moli_test.cursor()
    sql = """
        SELECT course_id, level, unit, selected_unitmask, teacher_id
        FROM main_class_ext
        WHERE class_course_id = %s
          AND start_time = %s
          AND classroom_status <> -1
    """
    cursor.execute(sql, (class_info, start_time))
    rows = cursor.fetchall()
    cursor.close()
    return rows

# 时间戳 -> 字符串
def ms2str(ms):
    return pd.to_datetime(ms, unit='ms').strftime('%Y-%m-%d %H:%M:%S')


# 1. 按 (classInfo, studentId) 聚合 startTime
group = defaultdict(list)
for item in get_csv():
    group[(item['classInfo'], item['studentId'])].append(item['startTime'])

# 2. 每个组合只发一次请求
for (class_info, student_id), start_times in group.items():
    full_course_info = []
    for time in start_times:
        db_rows = get_db_information(class_info, time)
        for row in db_rows:
            course_id, level, unit, selected_unitmask, teacher_id = row
            full_course_info.append({
                "course_id": str(course_id),
                "course_start_time": ms2str(time),
                "lesson": str(selected_unitmask),
                "unit": str(unit),
                "level": str(level - 8000),
                "teacher_id": teacher_id
            })

    if not full_course_info:
        continue

    payload = {
        "student_id": student_id,
        "operator_id": 667016,
        "operator_name": "农伟",
        "course_info_list": full_course_info,
        "class_id": class_info,
        "book_from": 6,
        "real_class_id": class_info
    }

    try:
        resp = requests.post(
            'https://sht-eos-gateway.vipthink.cn/course/combine/class/cambridge/student/course/add',
            json=payload, timeout=10
        )
        if resp.status_code != 200 or resp.json().get('code') != 0:
            print(f"FAIL class={class_info} student={student_id} 课程数={len(full_course_info)} response={resp.text}")
    except Exception as e:
        print(f"EXCEPT class={class_info} student={student_id} error={e}")

if __name__ == '__main__':
    print(get_csv())

