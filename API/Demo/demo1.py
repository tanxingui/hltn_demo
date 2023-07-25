import re
from datetime import datetime, timedelta
import requests

token = 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiekhhM2VFbGxsU2FlNTB3MVhqamgwQXBEVzllNDhxb0RVTCtHYXZxdWRrdTRGeXk0OEZBZVVNQWU2bFRSV1lBK0h2TGYrYWRrRTI2SURMTXVPK3RoSFZVNktZSWdvaFBUR0xaaUxBU1pkb3FLNFlzc3gwL3g2ZGdvQlFKZlhlNmFxODdMaUpPYzdTWHIwcDY2eXJ5WnFWMlNKb1dtUU8vV0pqWVFmUkVKOEhZZm4yS25wQnh6Vkx3Z3N4eDRMNS9kRFduNnNZdmJnQmNyTkx1T0RMeWQ2OHJYOXdDUDA4aWhmdkMyRXZlV28venQxZkRreHh3NWM5Rkp3d3lhSExycmtJak5KMVRWS0hybkZ3bC9tQ1VXMlE9PSIsImV4cCI6MTcwNTgzMTUzM30.c5x_IA3_NE518C-7jf-dQc2X6OXSzXFKlNZLV9s0w54'


def get_demo_course():
    url = "https://gw-mg-test.61info.cn/hll-leads-manager-provider/o/experience/student/specialCourse"
    payload = {
        "studentId": 22625430,
        "language": 1
    }
    header = {"authorization":
                  token
              }
    response = requests.post(url=url, data=payload, headers=header)
    course_ids = re.findall(r"'id': (\d+)", str(response.json()))
    course_names = re.findall(r"'name': (.+?),", str(response.json()))
    course_names = [name.strip("'") for name in course_names]
    return dict(zip(course_ids, course_names))


# 获取当前日期以为未来N天的年月日
def future_date(num_day):
    today = datetime.now().date()
    dates_list = []
    for i in range(num_day):
        future_date = today + timedelta(days=i)
        dates_list.append(future_date)
    return dates_list


# 获取有学位的课程id以及时间
def get_course_time():
    demo_courses = get_demo_course()
    dates_list = future_date(7)
    for course_id in demo_courses.keys():
        for date in dates_list:
            url = "https://gw-mg-test.61info.cn/hll-leads-manager-provider/o/teacher/schedule/v3/demo/student/preAppoint"
            payload = {
                "courseId": course_id,
                "courseDay": str(date),
                "classType": 2,
                "studentId": 22624527,
            }
            header = {
                "authorization": token
            }
            response = (requests.post(url=url, data=payload, headers=header)).json()['data']
            for item in response:
                if item.get('canAppointCount') == -1:
                    result_dict = {
                        "date": date,
                        "beginTime": item.get('beginTime')
                    }
                    time_str = result_dict['date'].strftime("%Y-%m-%d")
                    # return f"{time_str}" + " " + f"{result_dict['beginTime']}"
                    # 返回datetime类型的对象，否则接口不支持
                    return datetime.strptime(f"{time_str}" + " " + f"{result_dict['beginTime']}",
                                                      "%Y-%m-%d %H:%M")


print(get_course_time())
