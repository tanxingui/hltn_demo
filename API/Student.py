#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/06/20 11:47
# @Author : 新贵大人
描述:
"""

import threading
import time
import requests
import pymysql
from queue import Queue

Thread_num = 200
db = pymysql.connect(host="rm-2ze9tjvu49805vxbw.mysql.rds.aliyuncs.com", user="mmtest", password="Mmears2023",
                     database="db_support")
cursor = db.cursor()
sql = "SELECT soc.student_id FROM `student_ocean` so LEFT JOIN student_ocean_clt soc ON so.student_id = soc.student_id WHERE so.original_service_subject = 0 ORDER BY soc.student_id DESC limit 300;"
cursor.execute(sql)
results = [row[0] for row in cursor.fetchall()]
token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI1NiIsIm5hbWUiOiLosK3mlrDotLUiLCJzdXBwb3J0SWQiOm51bGwsImV4cCI6MTY4NzMxNTE2MiwiaWF0IjoxNjg3MjI4NzYyLCJlbWFpbCI6InRhbnhpbmd1aUBobHRuLmNvbSJ9.KuBTkr83K6lwas9qVGozlwI69b9c0bkj4Q_HFHcEorZTbfrVXAIwtyRVP9FFqZLSCIiPyA-FBw6D2lN1afHOkw'
new_list = []
lock = threading.Lock()


def worker(q: Queue):
    while True:
        student_id = q.get()
        url = "https://apistaging.mmears.com/customer/studentocean/searchbykeyword"
        headers = {
            'x-app-id': '2',
            'x-auth-token': token
        }
        data = {"keyword": student_id}
        try:
            response = requests.post(url, headers=headers, data=data)
            # 判断是否出现状态码异常
            response.raise_for_status()
            if response.json()["data"]:
                with lock:
                    new_list.append(student_id)
        except requests.exceptions.RequestException as e:
            print(f'请求出错，请检查网络连接，异常原因:{e}')
        q.task_done()


if __name__ == '__main__':
    q = Queue()
    for student_id in results:
        q.put(student_id)

    # 创建worker线程并启动
    start_time = time.time()
    for i in range(Thread_num):
        t = threading.Thread(target=worker, args=(q,))
        t.daemon = True
        t.start()
    q.join()
    end_time = time.time()
    print(f"完毕,耗时{(end_time - start_time):.2f}秒")
    print(new_list)