#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/07/16 15:01
# @Author : 新贵大人
描述:
"""
import datetime as dt
import time
import pymysql
import requests

mysql_ea_center_test = pymysql.connect(host='10.4.32.47', port=3306, user='shdev', password='6JrpIH4DbtE1w2YH',
                                       db='ea_center')


def get_big_course_name():
    now = dt.datetime.now().strftime('%y%m%d %H:%S')
    name = now + "大班直播课-xg"
    return name


def get_big_course_name():
    now = dt.datetime.now().strftime('%y%m%d %H:%S')
    name = now + "大班直播课-xg"
    return name


def big_course_date(num_day: int) -> str:
    return (dt.datetime.now() + dt.timedelta(days=num_day)).strftime("%Y-%m-%d 00:00:00")


def get_big_course_starttime():
    now = dt.datetime.now().strftime(f'%Y-%m-%d 00:00:00')
    return now


def get_big_course_endtime():
    now = dt.datetime.now().strftime(f'%Y-%m-%d 23:59:59')
    return now


def get_first_course_time(num_day):
    return (dt.datetime.now() + dt.timedelta(days=num_day)).strftime("%Y-%m-%d")


def special_course_teacher_name(name, nick):
    teacher_name = str(nick) + "(" + str(name) + ")"
    return teacher_name


def get_today_start_ms():
    today_start_ms = int(dt.datetime.combine(dt.date.today(), dt.datetime.min.time()).timestamp() * 1000)
    return today_start_ms


def get_target_ts_seconds(time_str: str) -> int:
    dt_obj = dt.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    return int(dt_obj.timestamp())


def today_timestamps(n):
    """
    获取今日 00:00:00 与 23:59:59 的秒级时间戳
    """
    today = dt.datetime.now().date()
    start = dt.datetime.combine(today, dt.datetime.min.time())
    end = dt.datetime.combine(today, dt.datetime.max.time()) - dt.timedelta(microseconds=1)
    if n == 0:
        return int(start.timestamp())
    return int(end.timestamp())


def get_class_courseId(token, class_id):
    url = "https://sht-eos-gateway.vipthink.cn/course/combine/class/cambridge/course/list"
    headers = {
        "authorization": token,
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    payload = {"class_id": class_id}

    try:
        resp = requests.get(url, params=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        courses = data.get("data", [])
        if len(courses) >= 2:
            return courses[1].get("course_id")
    except Exception:
        pass
    return None


def get_last_lul(token, class_id, num):
    url = "https://sht-eos-gateway.vipthink.cn/course/combine/class/cambridge/course/list"
    headers = {
        "authorization": token,
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    payload = {"class_id": class_id}
    resp = requests.get(url, params=payload, headers=headers, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    courses = data.get("data", [])
    # 取最后一个 course 的 lul
    lul = courses[-1].get("lul")
    parts = lul.split("-")
    if num == 1:
        return parts[0]
    elif num == 2:
        return parts[1]
    else:
        return parts[2]


def del_class_data(class_id):
    try:
        cursor = mysql_ea_center_test.cursor()
        delete_sql1 = f"DELETE FROM ea_center.ea_cambridge_class WHERE id = {class_id};"
        cursor.execute(delete_sql1)

        delete_sql2 = f"DELETE FROM ea_center.ea_cambridge_live_class_student WHERE class_id = {class_id};"
        cursor.execute(delete_sql2)

        mysql_ea_center_test.commit()
    except Exception as e:
        mysql_ea_center_test.rollback()
    finally:
        cursor.close()


def get_classstarttime(token, courseid):
    url = 'https://sht-eos-gateway.vipthink.cn/cc-backend/magicEars/course/page'
    header = {
        "authorization": token,
        "content-type": "application/json;charset=UTF-8"
    }
    payload = {
        "uuid": "12249773",
        "startTime": "",
        "endTime": "",
        "pageIndex": 1,
        "pageSize": 20
    }
    rsq = requests.post(url, headers=header, json=payload).json()
    for i in rsq['data']['records']:
        if i['courseId'] == courseid:
            return i['classStartTime']
    return


if __name__ == '__main__':
    print(get_classstarttime(
        "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzU5ODkxODYwLCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3NTk5NzgyNjAsImlhdCI6MTc1OTg5MTg2MCwic2lkIjoxfSx7InJhbmQiOiI3MTQ0MTQzODczNDY5NTgzNDE2NTk2MTc2NjE0MjM4NDI5NjM0NTY1NTUzODI2OTAxMzY0OTAzMjAxMjUzMzc5IiwidWlkIjo2Njc1MDgsInR5cCI6ImEiLCJ0aW1lIjoxNzU5ODkxODYwfV0.YWYwYjgxNDIyNmNiODFmZjhhYjlhMzhmOTMwNjQzMzM4Mjg1NTdlODkxZmVmNTdmZDc3Y2Y0YjU1OTliNTc3MA",
        '2025100817300000010229375'))
