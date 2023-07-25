import re
from datetime import datetime, timedelta
import requests

# 获取课程id以及对应的课程名称
def get_demo_course(host,studentId,accessToken):
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


# 获取当前日期以为未来N天的年月日
def future_date(num_day):
    today = datetime.now().date()
    dates_list = []
    for i in range(num_day):
        future_date = today + timedelta(days=i)
        dates_list.append(future_date)
    return dates_list

# 获取有学位的课程id以及时间
def get_course_time(host,studentId,accessToken):
    demo_courses = get_demo_course(host,studentId,accessToken)
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
                "authorization":accessToken
            }
            response = (requests.post(url=url, data=payload, headers=header)).json()['data']
            for item in response:
                if item.get('canAppointCount') == 1:
                    result_dict = {
                        "date": date,
                        "beginTime": item.get('beginTime')
                    }
                    time_str = result_dict['date'].strftime("%Y-%m-%d")
                    return [course_id, f"{time_str}"+" "+f"{result_dict['beginTime']}"]



#${get_course_time($mg_url,$hualala_id,$accessToken)}