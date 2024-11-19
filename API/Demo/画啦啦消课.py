#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/09/25 11:37
# @Author : 新贵大人
描述:
"""
import json
import requests



class Hualala_Script():

    def __init__(self,env_select):

        if env_select == "test":
            self.cms_url = "https://gw-mg-test.61info.cn"
        elif env_select == "preprod":
            self.cms_url = "https://gw-mg-preprod.61info.cn"
        else:
            print("input error")
        self.token = self.hualala_login()["token"]


    def hualala_login(self):
        url = self.cms_url + '/oa-user-center/sso/login'
        if env_select == "test":
            data = {
                "account": "19910256781",
                "password": "e10adc3949ba59abbe56e057f20f883e",
                "smsCode": "1234"
            }
        elif env_select == "preprod":
            data = {
                "account": "13250252197",
                "password": "e10adc3949ba59abbe56e057f20f883e",
                "smsCode": "1234"
            }
        else:
            data = {
                "account": "19910256781",
                "password": "e10adc3949ba59abbe56e057f20f883e",
                "smsCode": "1234"
            }

        res = requests.session().post(url=url, data=data)
        token = json.loads(res.text)["data"]["accessToken"]
        print(token)
        rps_data = {
            "token": token
        }
        return rps_data


    # 到课消课记录，查询待消课的记录
    def get_takeAndConsume_list(self,userid):

        url = self.cms_url + '/manager-api/o/course/takeAndConsume/getList'
        headers = {
            "authorization": self.token
        }
        params_data = {
                        "page":"1",
                        "size":"30",
                        "startDate": "2020-01-01",
                        "endDate": "2024-12-31",
                        "courseTimeScheduleId":0,
                        "workGroupId":0,
                        "teacherId":0,
                        "consumeStatus":0,
                        "courseType":0,
                        "userName":userid,
                        "groupName":"",
                        "belongArea":"",
                        "userId":"",
                        "teacherName":""
                       }
        res = requests.get(url=url, params=params_data,headers=headers)
        re_data = json.loads(res.text)["data"]["data"]


        for i in range(len(re_data)):
            id = json.loads(res.text)["data"]["data"][i]["id"]
            self.commit_manual_consume(id)
            i += 1



    # 到课消课记录，操作手动消课
    def commit_manual_consume(self,id):

        url = self.cms_url + '/manager-api/o/course/takeAndConsume/commitManualConsume'
        headers = {
            "authorization": self.token,
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "accept":"application/json, text/plain, */*"
        }
        data = {
                "id":id,
                "url":"https%3A%2F%2Fhualala-common.oss-cn-shenzhen.aliyuncs.com%2Ftest%2Fcms%2F6550cf8ef4edcc0001ac66df.png",
                "reason": "9512345678977777777",
                "type": 2
        }
        res = requests.session().post(url=url, data=data,headers=headers)
        print(json.loads(res.text))


    # 消课审核-查询接口
    def query_playback_record(self,userid):
        url = self.cms_url + '/manager-api/o/apply/playbackRecord/query.json'
        headers = {
            "authorization": self.token
        }
        data = {
                "groupId": 0,
                "teacherId": 0,
                "user": userid,
                "page": 1,
                "size": 100,
                "state": 1
        }
        res = requests.session().post(url=url, data=data,headers=headers)
        print(json.loads(res.text))
        re_data = json.loads(res.text)["data"]["list"]

        for i in range(len(re_data)):
            id = json.loads(res.text)["data"]["list"][i]["id"]
            self.agree_playback_record(id)
            i += 1



    # 同意消课审核
    def agree_playback_record(self,id):
        url = self.cms_url + '/manager-api/o/apply/playbackRecord/updateState.json'
        headers = {
            "authorization": self.token
        }
        data = {
                "id": id,
                "state": 2,
                "reason": "",
                "type": 2,

        }
        res = requests.session().post(url=url, data=data,headers=headers)
        print(json.loads(res.text))

    # 操作取消消课和同意消课审核
    def operate_student_cancel_classes(self,userid):
        self.get_takeAndConsume_list(userid)
        self.query_playback_record(userid)


if __name__ == '__main__':
    env_select = "test"  # 切换环境
    userid = 22560704  #修改学员id
    hualala_script = Hualala_Script(env_select)
    hualala_script.operate_student_cancel_classes(userid)   # 操作取消消课和同意消课审核



