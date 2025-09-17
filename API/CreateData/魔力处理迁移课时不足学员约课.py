#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/09/16 19:00
# @Author : 新贵大人
描述:
"""
import pandas as pd
import re
from curl_cffi import requests as ccurl_requests
import requests
from collections import defaultdict

# mysql_moli_test = pymysql.connect(host='172.23.59.64', port=3306, user='mmtest', password='Mmears2023',
#                                        db='db_course')
def get_csv():
    df = pd.read_csv(r'C:\Users\92101\Desktop\课时不足学员.csv')
    results = []
    # 正则
    class_info_pattern = re.compile(r'classInfo:(\d+)')
    start_time_pattern = re.compile(r'startTime:(\d+)')
    dto_pattern = re.compile(r'StudentBookResultDTO\([^)]+\)')

    for _, row in df.iterrows():
        message = row['message']
        if pd.isna(message):
            continue

        class_info = int(class_info_pattern.search(message).group(1))
        start_time = int(start_time_pattern.search(message).group(1))

        for dto in dto_pattern.findall(message):
            if 'bookCode=10' in dto and 'bookResult=学生课时不足' in dto:
                student_id = int(re.search(r'studentId=(\d+)', dto).group(1))
                results.append({
                    'classInfo': class_info,
                    'startTime': start_time,
                    'studentId': student_id
                })
    return results

# 生产没有数据库权限，改用调接口去dms查
# def get_db_information(class_info, start_time):
#     cursor = mysql_moli_test.cursor()
#     sql = """
#         SELECT course_id, level, unit, selected_unitmask, teacher_id
#         FROM main_class_ext
#         WHERE class_course_id = %s
#           AND start_time = %s
#           AND classroom_status <> -1
#     """
#     cursor.execute(sql, (class_info, start_time))
#     rows = cursor.fetchall()
#     cursor.close()
#     return rows


# 去dms查数据
def get_dms_data(class_info, start_time):
    headers = {
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'X-Token': 'd2admin-1.25.0-lang=zh-chs; d2admin-1.25.0-uuid=8690c68f-f9f3-4b49-bc34-6271db65dd8e; d2admin-1.25.0-token=47f8d22f-367a-44d7-bf3e-e472133dea6b',
        'sec-ch-ua-mobile': '?0',
        'Authorization': '47f8d22f-367a-44d7-bf3e-e472133dea6b',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Referer': 'https://ops-dms.hltn.com/',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        # 'instance_name': '魔力耳朵-rds-北京-prod-从库',
        'instance_name':'魔力耳朵北京测试库',
        'db_name': 'db_course',
        'schema_name': '',
        'tb_name': '',
        'sql_content': f'select course_id,level,unit,selected_unitmask,teacher_id from main_class_ext where class_course_id = {class_info} and start_time = {start_time} and classroom_status <> -1 limit 100;',
        'limit_num': 100,
    }
    resp = ccurl_requests.post(
        'https://ops-dms-backend.hltn.com/query/v1/query',
        headers=headers,
        json=json_data,
        impersonate="chrome123",
        timeout=30
    ).json()

    if resp.get("code") == 0 and resp.get("data"):
        rows = resp["data"].get("rows", [])
        cols = resp["data"]["column_list"]
        return [dict(zip(cols, row)) for row in rows]
    return []


# 毫秒时间戳转字符串
def ms2str(ms):
    return pd.to_datetime(ms, unit='ms', utc=True).tz_convert('Asia/Shanghai').strftime('%Y-%m-%d %H:%M:%S')

def main(url,token):
    # 按classInfo, studentId分组聚合startTime
    group = defaultdict(list)
    for item in get_csv():
        group[(item['classInfo'], item['studentId'])].append(item['startTime'])
    # 每个班级下面的课程对应的课时不足学员只发一次请求
    for (class_info, student_id), start_times in group.items():
        full_course_info = []
        for time in start_times:
            db_rows = get_dms_data(class_info, time)
            for row in db_rows:
                course_id = row["course_id"]
                level=row["level"]
                unit = row["unit"]
                selected_unitmask = row["selected_unitmask"]
                teacher_id = row["teacher_id"]
                print(type(level))
                full_course_info.append({
                    "course_id": str(course_id),
                    "course_start_time": ms2str(time),
                    "lesson": str(selected_unitmask),
                    "unit": str(unit),
                    "level": str(level - 80000),
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
        headers = {"authorization": token, 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}

        try:
            resp = requests.post(url=url, json=payload, headers=headers)
            if resp.status_code != 200 or resp.json().get('code') != 200:
                print(f"FAIL class={class_info} student={student_id} 课程数={len(full_course_info)} response={resp.json()}")
        except Exception as e:
            print(f"EXCEPT class={class_info} student={student_id} error={e}")

if __name__ == '__main__':
    print(main('https://sht-eos-gateway.vipthink.cn/course/combine/class/cambridge/student/course/add','111'))

