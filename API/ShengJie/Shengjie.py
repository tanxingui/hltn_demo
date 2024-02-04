import jsonpath
import pandas as pd
import requests
from ShengJie.Mysqlconfig import DBConnection
import json
import time

# 放初始学员
user_id_iii = [259097, 216412, 22460660, 22460654, 9999127, 9999269, 9999280, 9999608]
# 挑选最多相同星期几的学员
'''9999127,
9999269,
9999280,
9999608'''

# 鉴权
authorization = 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiSUNwa01oNTYxMDVmck92TE1yUmJRamFkdFJjSTBscWUxYytZZCt3SEJuL3RsblRUYWpIamhEdE0zWDBhSkhBTW1ZSmxEeGxaWWVZZVhMSkMzcmIzcFBCWU0yaVJBbGlHZnBnaE9UV1pNcXYwSlRZYXNvSEFaai9VUnFrd0s1aWUxcERBZlVwUzJYdDFaQXQ5M1RmRHBVYlBXVUE4YW1mMnRWMnVUTThlSVE4VnpLLy9aZFh1TVF5OTB0aytzSnMwMGlxc0pOMmVla3l1MjkwQlhWVTY5Uy9FajZtYi94eGNZT1dxZ2NwbkxsQ0ZUWnZ4YzBWaTc4bW1mOG9HVkk0cE9tamxTRFJNb01rNUoxWkw0WmgzUGc9PSIsImV4cCI6MTcxMjQ4MzcwMH0.p6pfh7YvMqrI8OxE0BrUk7wsap4haKKJ0s9YYn8QJm8'


# 查询学员是周几上课的,获取周期中最多学员上课的一日
def week():
    liebiao = []
    try:
        for i in user_id_iii:
            url = 'https://gw-mg-test.61info.cn/hll-uc-service/o/user/getFormalInfo/%s' % i
            headers = {
                'authorization': authorization
            }
            res = requests.get(url=url, headers=headers)
            week = jsonpath.jsonpath(res.json(), '$..week')
            liebiao.append(week[0])
        aaa = dict(zip(user_id_iii, liebiao))
        print(aaa)
        Dict1 = {}
        for m, n in aaa.items():
            if n not in Dict1:
                Dict1[n] = 0
            else:
                Dict1[n] += 1
        # 获取出现最多的value值对应的key
        for m, n in aaa.items():
            if n == max(Dict1, key=Dict1.get):
                user_Id.append(m)
        print(user_Id)
    except:
        raise '鉴权码要换个新的'


# 根据原班级的上课时间提交升阶分班意向
def apply():
    try:
        for i in user_Id:
            url1 = 'https://gw-mg-test.61info.cn/manager-api/o/advanced/allocation/application/getCurrentClassInfo?userId=%s' % i
            headers = {
                'content-type': 'application/json',
                'authorization': authorization
            }
            res1 = requests.get(url=url1, headers=headers)
            weeK = jsonpath.jsonpath(res1.json(), '$..week')[0]  # 获取原班级是星期几上课
            courseTimeId = jsonpath.jsonpath(res1.json(), '$..courseTimeId')[0]  # 获取原班级时间段对应的id
            url2 = 'https://gw-mg-test.61info.cn/manager-api/o/advanced/allocation/application/apply'
            payload = json.dumps({
                "weekDay": weeK,
                "courseTimeScheduleId": courseTimeId,
                "userId": i
            })
            rsp = requests.post(url=url2, data=payload, headers=headers)
            print(rsp.json())
    except TypeError:
        print("换个token")


# 查询所在班级id
def groupId():
    group_id = []
    for i in user_Id:
        hu = DBConnection().select("select group_id FROM user_group_relation where user_id = %s" % i)
        group_id.append(hu[0][0])
    # print(group_id)
    # for p in group_id:
    #     ooo = DBConnection().select("select teacher_id from group_teach_relation WHERE group_id = %s " % p)
    #     print("{}的授课老师id是:".format(i), ooo)
    return group_id


# 修改成相同的授课老师 teacher_id = 100077   100060   100057   100066  200009   400474
def updateteacher(AAA):
    for i in groupId():
        DBConnection().update("UPDATE group_teach_relation set teacher_id = %s where group_id = %s" % (AAA, i))


# 修改年龄
def age():
    birthday = '2015-05-01'
    for user_Ids in user_Id:
        DBConnection().update(
            "update allocation_application set birth_month = '%s' where user_id = %s" % (birthday, user_Ids))
        # DBConnection().update("update i61.userinfo set BirthMonth = '%s' where UserId = %s" % (birthday, user_Ids))


# 修改课耗：
def kehao():
    liebiao = []
    try:
        for kehao in user_Id:
            keshi_id = DBConnection().select(
                "select id from group_user_course_schedule_info where user_id = %s" % kehao)
            for kehao1 in keshi_id:  # 元祖转成列表
                kehao2 = kehao1[0]
                liebiao.append(kehao2)
        for xxx in liebiao:
            DBConnection().update(
                "update group_user_course_schedule_info set teacher_consume_time = '2022-10-19', consume_status = 1 where id = %s" % xxx)
    except:
        print('数据修改失败')


# 修改扩班意向为八人班
def group_size():
    for i in user_Id:
        DBConnection().update("update allocation_application_advance set group_size = 6 where user_id = %s" % i)


# 修改意向课程等级 L1=1  L2=5  L3=9  L4=13  L5=17  L6=21 5：高阶-经典艺术 6：高阶-设计艺术   页面上改
def level(dengji):
    for i in user_Id:
        DBConnection().update(
            "update allocation_application_advance set begin_course_stage_id = %s where user_id = %s" % (dengji, i))


# 修改意向班级、意向时段   意向班级：28普通班，30中英班，31咕比班，29粤语班
def Class(yixiangbanji,week):
    cursor = DBConnection().getCon().cursor()  # 创建游标对象
    # 调接口获取页面上展示的时间段
    url = 'https://gw-mg-test.61info.cn/manager-api/o/advanced/allocation/application/getAdvancedAllocateDateTimeList?userId=22560489&intentGroup=0'
    headers = {
        'authorization': authorization
    }
    res = requests.get(url=url, headers=headers)
    timeId = jsonpath.jsonpath(res.json(), '$..timeId')  # 查询时间段id
    begin_time_liebiao = list(set(timeId))
    # # 随机从列表中选5个时间段
    # begin_time =  random.sample(begin_time_liebiao,5)
    tuple_time = tuple(begin_time_liebiao)
    # 随机查询可用的时间段id对应的时间段
    sql = '''select id,begin_time,end_time from course_time_schdule where state = 0 and course_type = 1 and id in {}'''.format(
        tuple_time)
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),
                      columns=['id', 'begin_time', 'end_time'])
    print(df)
    input_id = input("输入你要的时间段id：")
    for i in user_Id:  # 修改升阶分班班级的时间、意向班级，时段前端页面不会改变
        DBConnection().update(
            "update allocation_application_advance set intent_group = %s , course_time_schedule_id = %s where user_id = %s" % (
                yixiangbanji, input_id, i))
    for i in groupId():  # 修改原班级的时间
        DBConnection().update("update group_info set course_time_id = %s where id = %s" % (input_id, i))
        DBConnection().update("update group_week_time_relation set time = %s,week = %s where group_id = %s" % (input_id, week, i))
    cursor.close()


# 撤销升阶已选择
def cancelApply():
    user_Idlist = []
    user_id = DBConnection().select(
        "SELECT a.user_id from allocation_application a left join allocation_application_advance b on a.user_id = b.user_id where b.state = 2 and b.group_size > 0")
    for user in user_id:  # 元祖转成列表
        user2 = user[0]
        user_Idlist.append(user2)
    len_userid = len(user_Idlist)
    print("本次要撤销升阶已选择的是:{}".format(user_Idlist), end='\n'
                                                     "一共要撤销{}个学员".format(len_userid))
    print()
    input_a = input('是否要执行撤销操作--- 1:是,2:否:')
    # 不要误删别人造的数据
    if input_a == "2":
        print('取消撤销')
    elif input_a == "1":
        for i in user_id:
            url = 'https://gw-mg-test.61info.cn/manager-api/o/advanced/allocation/application/cancelApply?userId=%s' % i
            headers = {
                'authorization': authorization
            }
            requests.get(url=url, headers=headers)
    else:
        print('请输入：1或2')


if __name__ == '__main__':
    bengin_time = time.time()
    print('开始修改')
    user_Id = [22620912,22621788,22621831]
    # week()  # 查询学员是周几上课的,获取周期中最多学员上课的一日
    apply()  # 提交升阶分班
    # groupId()  # 查询所在班级id
    updateteacher(400474)  # 修改成相同的授课老师 teacher_id = 100077   100060   100057   100066   100029  201922  100061
    # age()  # 修改年龄
    # kehao()   # 修改课耗
    # group_size()  # 修改扩班意向为八人班
    level(9)  # 修改意向课程等级 L1=1  L2=5  L3=9  L4=13   高阶-经典艺术=17  高阶-设计艺术=21
    Class(28,2)  # 修改意向班级、意向时段   意向班级：28普通班，30中英班，31咕比班，29粤语班   后面这个参数是周几
    # cancelApply()  # 撤销升阶已选择
    print('修改完毕')
    end_time = time.time()
    print('本次耗时：', '%.2f' % (end_time - bengin_time), "秒", sep='')




