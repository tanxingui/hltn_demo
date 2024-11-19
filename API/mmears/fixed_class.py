#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/12/05 20:42
# @Author : 新贵大人
描述:
"""
# 生成当前时间的毫秒时间戳
import base64
import datetime
import time
import random
import pymysql
import requests


def date_unix_time(days):
    # 获取当前对象
    time_tuple = (datetime.datetime.now().date() + datetime.timedelta(days=days)).timetuple()
    # 将时间元组转换为时间戳
    unix_timestamp = time.mktime(time_tuple)
    # 时间戳转换为毫秒级时间戳
    unixtime = round(unix_timestamp * 1000)
    return unixtime


def datetime_moli(days):
    # 获取当前对象
    time_tuple = datetime.datetime.now().date() + datetime.timedelta(days=days)
    return str(time_tuple) + " " + "00:00:00"

def get_fixclassid(studentId, token):
    global starttime
    payload = {
        "studentId": studentId,
        "pageIndex": 1,
        "pageSize": 20
    }
    headers = {"X-App-Id": "2",
               "X-Auth-Token": token}
    try:
        starttime = time.time()
        for i in range(5):
            response = requests.post("https://apistaging.mmears.com/customer/fixed/course/getStudentFixedList",
                                     json=payload, headers=headers)
            courseId = response.json()['data']['records'][0]['courseId']
            if courseId:
                # 执行固班约课脚本
                rsp = requests.get(f"https://apistaging.mmears.com/course-service/bookSingle?courseId={courseId}",
                                   headers=headers)
                if rsp.status_code == 200:
                    tuple1 = "OK", courseId
                    return [i for i in tuple1]
            if i < 4:
                print(f"第 {i + 1} 次查询无数据，等待 60 秒后次查询!")
                time.sleep(1)
            else:
                print("查询 5 次均无数据，该学员未成班!")
                return 201

    except Exception as e:
        print("报错信息：", e)
    finally:
        endtime = time.time()
        print('本次耗时：', '%.2f' % (endtime - starttime), "秒", sep='')


# print(get_fixclassid(4649220,                "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI1NiIsIm5hbWUiOiLosK3mlrDotLUiLCJzdXBwb3J0SWQiOm51bGwsImV4cCI6MTcwMjM0ODg1NywiaWF0IjoxNzAyMjYyNDU3LCJlbWFpbCI6InRhbnhpbmd1aUBobHRuLmNvbSJ9.mLvXLcZ3DNN6cyb19k61JgJfMZa0bfKbiYGJyVjWlaVy7JxwZhAmJhAQM_nQv4oXlFoJ3XQgGde9vQjsFI_Unw"))


def get_teacher_id(token):
    global teacher_id
    query_url = "https://apistaging.mmears.com/teacher/contract/renew/query"
    class_url = "https://apistaging.mmears.com/teacher/fixed/class/page"
    header = {"X-App-Id": "6", "X-Auth-Token": token}

    payload1 = {"expireStartTime": f"{date_unix_time(-150)}", "expireEndTime": f"{date_unix_time(0)}",
                "renewalStatus": "NOT_RENEWAL", "pageIndex": 1, "pageSize": 100}
    response1 = requests.post(query_url, headers=header, json=payload1)
    if response1.status_code == 200:
        teacher_id = response1.json()['data']['records'][0]['teacherId']
    payload2 = {"pageIndex": 1, "pageSize": 50, "teacherId": teacher_id}
    response2 = requests.post(class_url, headers=header, json=payload2)
    if response2.json()['data']['records']:
        mysql_conn = pymysql.connect(host='172.23.59.64', port=3306, user='mmtest', password='Mmears2023',
                                     db='db_teacher')
        cursor = mysql_conn.cursor()
        sql = f"delete from teacher_fixed_class where teacher_id = {teacher_id};"
        try:
            cursor.execute(sql)
            mysql_conn.commit()
        except Exception as e:
            mysql_conn.rollback()
            print("数据删除失败：", e)
        finally:
            cursor.close()
            mysql_conn.close()
    return teacher_id

def add_fixed_teacher_banci(token,teacherId):
    url = "https://apistaging.mmears.com/teacher/fixed/class/saveTeacherFixedTimePeriod"
    data = {'saveFixedCourseDTO': [{'week': 6, 'timeId': 1}, {'week': 7, 'timeId': 1}], 'teacherId': teacherId}
    header = {"X-Auth-Token": token, "X-App-Id": "6"}
    while True:
        try:
            response = requests.post(url, json=data, headers=header).json()
            if response["code"] == "OK":
                return 1
            elif response["code"] == "BIZ_FAIL":
                time.sleep(5)  # 等待5秒后继续调用该接口
            else:
                raise Exception("接口执行错误，并非排课中")
        except Exception as e:
            print("Error: ", e)
            time.sleep(5)  # 等待5秒后重试


def get_fixclassid1(studentId, clp_token):
    payload = {"user_id": studentId}
    clp_headers = {"Authorization": clp_token}
    try:
        for i in range(30):
            response = requests.post("https://sht-eos-gateway.vipthink.cn/eos-lp/student/detail",
                                     json=payload, headers=clp_headers)
            courseId = response.json()["stu_info"]["mmears_info"]["fixed_course_id"]
            if courseId:
                return str(courseId)
            if i < 29:
                print(f"第 {i + 1} 次查询无数据，等待 60 秒后次查询!")
                time.sleep(10)
            else:
                print("查询 30 次均无数据，该学员未成班!")
                return 201
    except Exception:
        print("报错信息：", response.json()["info"])

if __name__ == '__main__':
    print(get_fixclassid1(18028578,
                          "Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzE5OTk4NTE2LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3MjAwODQ5MTYsImlhdCI6MTcxOTk5ODUxNiwic2lkIjoxfSx7InJhbmQiOiI3MjIzMDk0NjE1NzQ0ODc4NDU4ODIxOTA1NzI1MjI2ODUyODQxMDA2NTI4MDMxMTkxMzg1NzQ1MTk3OTcwMDQ0IiwidWlkIjo2Njc1MDgsInR5cCI6ImEiLCJ0aW1lIjoxNzE5OTk4NTE2fV0.YmFiZDRjYjNhMzdkOTEwNzAwMzcyNDBjMGMwNWY1OWM2NDBiZjc4NTAwZTQ0NWQ5YzU1MTBjMmEzMzNkMzcyYQ"))