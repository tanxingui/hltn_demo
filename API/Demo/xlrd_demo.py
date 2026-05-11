# import xlrd
# import os
#
# parent_path = os.path.dirname(__file__)
# excel_path = os.path.join(parent_path, 'tttt.xls')
#
# # 根据行名跟列名拿到对应单元格数据
# def get_excel_data(rowdata, coldata):
#     workbook = xlrd.open_workbook(excel_path)
#     sheet = workbook.sheet_by_name('Sheet1')
#     col_index = None
#     row_index = None
#     # nrow = sheet.nrows    #获取行数
#     ncol = sheet.ncols    # 获取列数
#     workcol = sheet.col_values(1)    # 获取第一列
#     for i in range(ncol):
#         if (sheet.cell_value(0, i) == coldata):
#             col_index = i  # 获取列标
#             break
#     for i in workcol:
#         if rowdata == i:
#             row_index = workcol.index(rowdata)  # 获取行号
#             break
#     data = sheet.cell_value(row_index, col_index)
#     return data
#
#
# print(get_excel_data('登陆成功', 'data'))
#
#


import datetime
import pymysql
import requests

def get_datetime_onehour():
    current_time = datetime.datetime.now()
    before_one_hour = current_time - datetime.timedelta(hours=1)
    before_one_hour_str = before_one_hour.strftime('%Y-%m-%d %H:%M:%S')
    return before_one_hour_str

# 获取今天是周几
def get_nowweek():
    current_time = datetime.datetime.now()
    week = current_time.weekday()+1
    return week

def update_coursedata(group_id):
    mysql_conn = pymysql.connect(host='db.preprod.61draw.com', port=3306, user='root', password='dbtest', db='i61-hll-manager')
    cursor = mysql_conn.cursor()
    sql = f"UPDATE `i61-hll-manager`.`group_course_schedule_info` SET `course_date` = '{get_datetime_onehour()}' WHERE group_id = {group_id};"
    try:
        cursor.execute(sql)
        mysql_conn.commit()
    except Exception as e:
        mysql_conn.rollback()
        print("数据修改失败：", e)
    finally:
        cursor.close()
        mysql_conn.close()


def get_xiaoke_id(authorization,user_id,group_id):
    update_coursedata(group_id)
    url = f'https://gw-mg-preprod.61info.cn/manager-api/o/course/takeAndConsume/getList?page=1&size=10&courseTimeScheduleId=0&workGroupId=0&teacherId=0&consumeStatus=-1&courseType=0&userName={user_id}&groupName=&belongArea=&userId=&teacherName='
    headers = {
        'content-type': 'application/json',
        'authorization': authorization
    }
    return requests.get(url=url, headers=headers).json()['data']['data'][0]['id']
# print(get_xiaoke_id("eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoicFVybUF1ZUVsRys5cEV5Q2x3YVM4dy9HeTRaSmRyaWRvS1kya0F5T0hsd09QMnpORjBXUHpJblU4c0hUaDNYWFFUdXNjWndkZFp0MEpDR2hsYjRjMHEwYm8xMjFvcmo5VEthSnphRGNLanh4VmZPTTFGc3pJZDNRS1ZqV3UwV2IwYmt6ZjJrSTlySElCRmdITEFrN0lNSlFaeWUyVDk0c0d2eWxUTmhSL3Q4Zjg2ZEFQWnZzY29wSUdqdStnaTVPdWVQM3o4VXkvbWFEcWJ2dmZ3c1d4Z2UyQU90NUlJMHpLZndWVmhrTFY1YmdDcnRDTC9PVFcyNTQ3cDBTS1l4Q2JvblhDcFFCZ0gxUDZXODJwbUFpaFE9PSIsImV4cCI6MTcwOTk4MTY2MX0.y4MHzos7zqvunNw5kN4XmbDxGhFIZC3Nx1Gy984bqo4","1394389"))