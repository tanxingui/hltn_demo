import re
import datetime as dt
import requests
import pymysql

mysql_conn = pymysql.connect(host='db.preprod.61draw.com', port=3306, user='root', password='dbtest',
                             db='i61-hll-manager')
mysql_conn1 = pymysql.connect(host='db.preprod.61draw.com', port=3306, user='root', password='dbtest', db='i61')


# 获取课程id以及对应的课程名称
def get_demo_course(host, studentId, accessToken):
    url = f"{host}/hll-leads-manager-provider/o/experience/student/specialCourse"
    payload = {
        "studentId": studentId,
        "language": 1
    }
    header = {
        "authorization": accessToken
    }
    response = requests.post(url=url, data=payload, headers=header)
    course_ids = re.findall(r"'id': (\d+)", str(response.json()))
    course_names = re.findall(r"'name': (.+?),", str(response.json()))
    course_names = [name.strip("'") for name in course_names]
    return dict(zip(course_ids, course_names))


# 获取当前日期以及未来N天的年月日
def future_date(num_day):
    today = dt.datetime.now().date()
    dates_list = []
    for i in range(num_day):
        future_date = today + dt.timedelta(days=i)
        dates_list.append(future_date)
    return dates_list


# 获取有学位的课程id
def get_courseid(host, studentId, accessToken):
    demo_courses = get_demo_course(host, studentId, accessToken)
    dates_list = future_date(7)
    for course_id in demo_courses.keys():
        for date in dates_list:
            url = f"{host}/hll-leads-manager-provider/o/teacher/schedule/v3/demo/student/preAppoint"
            payload = {
                "courseId": course_id,
                "courseDay": str(date),
                "classType": 2,
                "studentId": studentId,
            }
            header = {
                "authorization": accessToken
            }
            response = (requests.post(url=url, data=payload, headers=header)).json()['data']
            for item in response:
                if item.get('canAppointCount') == 1:
                    result_dict = {
                        "date": date,
                        "beginTime": item.get('beginTime')
                    }
                    time_str = result_dict['date'].strftime("%Y-%m-%d")
                    return course_id


# 获取课程时间
def get_coursetime(host, studentId, accessToken):
    demo_courses = get_demo_course(host, studentId, accessToken)
    dates_list = future_date(7)
    for course_id in demo_courses.keys():
        for date in dates_list:
            url = f"{host}/hll-leads-manager-provider/o/teacher/schedule/v3/demo/student/preAppoint"
            payload = {
                "courseId": course_id,
                "courseDay": str(date),
                "classType": 2,
                "studentId": studentId,
            }
            header = {
                "authorization": accessToken
            }
            response = (requests.post(url=url, data=payload, headers=header)).json()['data']
            for item in response:
                if item.get('canAppointCount') == 1:
                    result_dict = {
                        "date": date,
                        "beginTime": item.get('beginTime')
                    }
                    time_str = result_dict['date'].strftime("%Y-%m-%d")
                    # 这里要返回datetime类型的对象，否则接口不支持
                    return dt.datetime.strptime(f"{time_str}" + " " + f"{result_dict['beginTime']}",
                                                "%Y-%m-%d %H:%M")


# 获取当前时间
def today_date():
    today = dt.datetime.now().date()
    return str(today)


# 获取n天后的时间
def future_num_date(num_day):
    future_date = dt.datetime.now().date() + dt.timedelta(days=num_day)
    return str(future_date)


# 批量取消上课
URL_LIST_STUDENT = "https://preprod-ems.vipthink.cn/gateway/route__jw/api/live_student/listStudent"
URL_CANCEL_LIVE = "https://preprod-ems.vipthink.cn/gateway/route__jw/work/live_student/cancel"

HEADERS = {
    "Origin": "https://preprod-crm.vipthink.cn",
    "Content-Type": "application/json;charset=UTF-8"
}


def cancel_live(lesson_id, Authorization):
    try:
        all_students = []
        for page_num in range(1, 20):
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


# 删除对应的老生开班批次
def delete_batch():
    cursor = mysql_conn.cursor()
    sql = "SELECT * FROM allocation_batch WHERE type = 3 AND NOW() BETWEEN begin_time AND end_time;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            for row in results:
                batch_id = row[0]
                delete_sql = f"DELETE FROM allocation_batch WHERE id = {batch_id};"
                cursor.execute(delete_sql)
                mysql_conn.commit()
                # print("批次:{},删除成功".format(batch_id))
                return 1
        else:
            print("未找到匹配的批次")
            return 1
    except Exception as e:
        return f"查询出错：{str(e)}"
    finally:
        cursor.close()
        mysql_conn.close()


# 删除对应的新生开班批次
def delete_new_batch():
    cursor = mysql_conn.cursor()
    sql = "SELECT * FROM allocation_batch WHERE type = 1 AND NOW() BETWEEN begin_time AND end_time;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            for row in results:
                batch_id = row[0]
                delete_sql = f"DELETE FROM allocation_batch WHERE id = {batch_id};"
                cursor.execute(delete_sql)
                mysql_conn.commit()
                # print("批次:{},删除成功".format(batch_id))
                return 1
        else:
            print("未找到匹配的批次")
            return 1
    except Exception as e:
        return f"查询出错：{str(e)}"
    finally:
        cursor.close()
        mysql_conn.close()


# 查找符合升阶的L1的学员
def get_level_one_student(sort):
    cursor1 = mysql_conn.cursor()
    cursor2 = mysql_conn1.cursor()

    try:
        sql1 = """
            SELECT DISTINCT ugr.user_id
            FROM `i61-hll-manager`.user_group_relation ugr
            JOIN `i61-hll-manager`.group_info gi ON ugr.group_id = gi.id
            JOIN `i61-hll-manager`.allocation_application aa ON ugr.user_id = aa.user_id
            JOIN `i61-hll-manager`.group_table_relation gtr ON ugr.group_id = gtr.group_id AND gtr.state = 0
            JOIN `i61-hll-manager`.course_table ct ON gtr.table_id = ct.id
            JOIN `i61-hll-manager`.course_begin_stage_info cbsi ON ct.begin_course_stage_id = cbsi.id
            LEFT JOIN `i61-hll-manager`.allocation_application_advance aaa ON aaa.user_id = ugr.user_id
            WHERE cbsi.years = 1
            AND ugr.group_id > 0
            AND gtr.state = 0
            AND (aaa.state = 1 OR aaa.id IS NULL)
            AND aa.state = 7
            ORDER BY RAND() DESC
            LIMIT 20;
        """

        cursor1.execute(sql1)
        student_ids = [row[0] for row in cursor1.fetchall()]
        student_ids_str = ','.join(map(str, student_ids))

        if not student_ids:
            return []

        sql2 = f"""
            SELECT UserId
            FROM i61.usercoursepackageinfo cpi
            WHERE cpi.UserId IN ({student_ids_str}) AND cpi.State < 4
            GROUP BY UserId
            HAVING SUM(cpi.CourseNumber) + SUM(cpi.GiftCourseNumber) - SUM(cpi.OpenCourseNumber) - SUM(cpi.OpenGiftCourseNumber) > 0
            LIMIT 3;
        """

        cursor2.execute(sql2)
        selected_students = [row[0] for row in cursor2.fetchall()]

        if not selected_students:
            return []

        sql3 = f"""
            SELECT * FROM `i61-hll-manager`.allocation_application_old
            WHERE user_id = {selected_students[sort - 1]};
        """
        cursor1.execute(sql3)
        results3 = cursor1.fetchall()

        if results3:
            sql4 = f"""
                DELETE FROM `i61-hll-manager`.allocation_application_old
                WHERE user_id = {selected_students[sort - 1]};
            """
            cursor1.execute(sql4)
            mysql_conn.commit()

        cursor1.close()
        cursor2.close()
        mysql_conn.close()
        mysql_conn1.close()

        if sort in [1, 2, 3]:
            return selected_students[sort - 1] if len(selected_students) >= sort else None
        return selected_students

    except Exception as e:
        print(f"发生错误: {e}")
        cursor1.close()
        cursor2.close()
        mysql_conn.close()
        mysql_conn1.close()


# 获取未来时间最近的一个周几的时间
def get_week_day(weekday):
    current_date = dt.datetime.now().date()
    current_weekday = current_date.weekday()
    days_until_target = weekday - current_weekday - 1
    if days_until_target <= 0:
        days_until_target += 7
    nearest_target_date = current_date + dt.timedelta(days=days_until_target)
    nearest_target_date_formatted = nearest_target_date.strftime("%Y-%m-%d")
    return nearest_target_date_formatted


# 删除强化课对应的开班批次
def delete_enhance_batch():
    cursor = mysql_conn.cursor()
    sql = "SELECT * FROM allocation_batch WHERE type = 4 AND NOW() BETWEEN begin_time AND end_time;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            for row in results:
                batch_id = row[0]
                delete_sql = f"DELETE FROM allocation_batch WHERE id = {batch_id};"
                cursor.execute(delete_sql)
                mysql_conn.commit()
                # print("批次:{},删除成功".format(batch_id))
                return 4
        else:
            print("未找到匹配的批次")
            return 4
    except Exception as e:
        return f"查询出错：{str(e)}"
    finally:
        cursor.close()
        mysql_conn.close()


# 修改强化课批次的分班结束时间为当天，不然强化课分班不成功
def enhance_batch_endtime(batch_id):
    try:
        today = dt.datetime.now().date()
        end_of_today = dt.datetime.combine(today, dt.time(23, 59, 59))
        cursor = mysql_conn.cursor()

        update_sql1 = """
            UPDATE `i61-hll-manager`.allocation_batch
            SET end_time = %s
            WHERE id = %s;
        """
        cursor.execute(update_sql1, (end_of_today, batch_id))

        update_sql2 = """
            UPDATE `i61-hll-manager`.allocation_batch_consequence_detail
            SET allocation_date = %s
            WHERE batch_id = %s;
        """
        cursor.execute(update_sql2, (end_of_today, batch_id))

        mysql_conn.commit()

    except Exception as e:
        mysql_conn.rollback()
        return f"更新失败：{str(e)}"

    finally:
        cursor.close()
        mysql_conn.close()

    return 1


# 获取开班批次需要开的时段id
def get_batch_detailId(host, batch_id, token, time_id):
    url = f"{host}/manager-api/o/new/applyAllocate/getBatchDetail.json"
    headers = {"authorization": token, 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    payload = f'batchId={batch_id}&needRecommendGroupCount=0'
    resp = requests.post(url, data=payload, headers=headers, timeout=8).json()
    # 提取timeId为96的数据
    time_data = next((item for item in resp['data']['dataList'] if item['timeId'] == time_id), None)
    # 如果找到了timeId的数据，提取周一的detailId
    if time_data:
        detail_id = next((vo['detailId'] for vo in time_data['voList'] if vo['dayForWeek'] == 1), None)
        return detail_id


# 更新强化课学员的已选分班状态
def update_allocation_application_enhance_state(student_id):
    try:
        cursor = mysql_conn.cursor()
        # 使用参数化查询来防止SQL注入
        update_sql = """
            UPDATE `i61-hll-manager`.allocation_application_enhance
            SET state = 1
            WHERE user_id = %s;
        """
        cursor.execute(update_sql, student_id)
        mysql_conn.commit()
    except Exception as e:
        return f"更新失败：{str(e)}"
    finally:
        cursor.close()
        mysql_conn.close()
    return 1