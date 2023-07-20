import re
from datetime import datetime, timedelta
import requests


def get_demo_course():
    url = "https://gw-mg-test.61info.cn/hll-leads-manager-provider/o/experience/student/specialCourse"
    payload = {
        "studentId": 22624518,
        "language": 1
    }
    header = {
        "authorization": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiSUNwa01oNTYxMDVmck92TE1yUmJRamFkdFJjSTBscWUxYytZZCt3SEJuK3FRcnRoWHh0ZTdMZm40cFpUMFpCNW1ZSmxEeGxaWWVZZVhMSkMzcmIzcENGQ0ZiRmhIM1JOR0VjR1RiOFl1SGVtNWhvOVhFZWkzY2FyTjlpNUtnSmpGUGJvWTZmZHpUYTFQWmE4UktudFoxdEpjM2J3TnVCN0loUFFwTUxRMmphb1I2MnIxQnZEMXM2TVpTYTB6eVZNYldUTnJJWTdSMlE5NTI0NFFHdmc0UFRRcFcyOVB3ejlqYXNVeHQ3clRLU3AxcHFZM1NId0ZUSXJyRWxrTUFCTDBjY3RTUmVKZ1cwZ2hYbFluWmI2OWc9PSIsImV4cCI6MTcwNTM4Njc3MX0.SbkukqZBUsJxwgVU0QxDgvGwvWZs1LK8XUvfIttKmlU"
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
                "authorization": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiSUNwa01oNTYxMDVmck92TE1yUmJRamFkdFJjSTBscWUxYytZZCt3SEJuK3FRcnRoWHh0ZTdMZm40cFpUMFpCNW1ZSmxEeGxaWWVZZVhMSkMzcmIzcENGQ0ZiRmhIM1JOR0VjR1RiOFl1SGVtNWhvOVhFZWkzY2FyTjlpNUtnSmpGUGJvWTZmZHpUYTFQWmE4UktudFoxdEpjM2J3TnVCN0loUFFwTUxRMmphb1I2MnIxQnZEMXM2TVpTYTB6eVZNYldUTnJJWTdSMlE5NTI0NFFHdmc0UFRRcFcyOVB3ejlqYXNVeHQ3clRLU3AxcHFZM1NId0ZUSXJyRWxrTUFCTDBjY3RTUmVKZ1cwZ2hYbFluWmI2OWc9PSIsImV4cCI6MTcwNTM4Njc3MX0.SbkukqZBUsJxwgVU0QxDgvGwvWZs1LK8XUvfIttKmlU"
            }
            response = (requests.post(url=url, data=payload, headers=header)).json()['data']
            for item in response:
                if item.get('canAppointCount') == -1:
                    result_dict = {
                        "date": date,
                        "beginTime": item.get('beginTime')
                    }
                    time_str = result_dict['date'].strftime("%Y-%m-%d")
                    return [course_id, f"{time_str}" + " " + f"{result_dict['beginTime']}"]


print(get_course_time())
