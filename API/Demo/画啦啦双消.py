#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/04/16 15:56
# @Author : 新贵大人
描述:
"""
import pymysql
import datetime

mysql_conn = pymysql.connect(host='db.preprod.61draw.com', port=3306, user='root', password='dbtest',
                             db='i61-hll-manager')
mysql_conn1 = pymysql.connect(host='db.preprod.61draw.com', port=3306, user='root', password='dbtest', db='i61')

# 获取当前批次，如果存在则删除
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

# 获取level的学员id，可用于提交升阶组班意向的
def get_level_one_student(sort):
    cursor1 = mysql_conn.cursor()
    cursor2 = mysql_conn1.cursor()

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
            GROUP BY ugr.user_id
            ORDER BY ugr.user_id DESC
            LIMIT 10;
        """

    results2_list = []

    # 循环找到3个学员
    while len(results2_list) < 3:
        cursor1.execute(sql1)
        results1 = cursor1.fetchall()
        student_id = [i[0] for i in results1]
        student_ids_str = ','.join(map(str, student_id))

        sql2 = """
                SELECT UserId
                FROM i61.usercoursepackageinfo cpi
                WHERE cpi.UserId IN ({}) AND cpi.State < 4
                GROUP BY UserId
                HAVING SUM(cpi.CourseNumber) + SUM(cpi.GiftCourseNumber) - SUM(cpi.OpenCourseNumber) - SUM(cpi.OpenGiftCourseNumber) > 0
                LIMIT 3;
            """.format(student_ids_str)

        cursor2.execute(sql2)
        results2 = cursor2.fetchall()

        # 将结果添加到列表中
        results2_list.extend(results2)

    cursor1.close()
    cursor2.close()
    mysql_conn.close()
    mysql_conn1.close()
    if sort == 1:
        return [i[0] for i in results2_list][0]
    elif sort == 2:
        return [i[0] for i in results2_list][1]
    elif sort == 3:
        return [i[0] for i in results2_list][2]
    else:
        return [i[0] for i in results2_list]

# 获取未来时间最近的一个周几的时间
def get_week_day(weekday):
    # 获取当前日期
    current_date = datetime.datetime.now().date()
    # 获取当前日期是星期几
    current_weekday = current_date.weekday() + 1
    days_until_saturday = weekday - current_weekday
    nearest_saturday = current_date + datetime.timedelta(days=days_until_saturday)
    nearest_saturday_formatted = nearest_saturday.strftime("%Y-%m-%d")
    return nearest_saturday_formatted

def future_date(num_day):
    today = datetime.datetime.now().date()
    dates_list = []
    for i in range(num_day):
        future_date = today + datetime.timedelta(days=i)
        dates_list.append(future_date)
    return dates_list

if __name__ == '__main__':
    # print(get_level_one_student(1))
    print(get_week_day(6))
