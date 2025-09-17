import http.client
import json

conn = http.client.HTTPSConnection("ops-dms-backend.hltn.com")
payload = json.dumps({
   "instance_name": "魔力耳朵-rds-北京-prod-从库",
   "db_name": "db_course",
   "schema_name": "",
   "tb_name": "",
   "sql_content": "select course_id,level,unit,selected_unitmask,teacher_id from main_class_ext where class_course_id = 792 and start_time = 1760007600000 and classroom_status <> -1 limit 100;\r\n",
   "limit_num": 100
})
headers = {
   'X-Token': 'd2admin-1.25.0-lang=zh-chs; d2admin-1.25.0-uuid=9571e985-cdb9-409c-a797-a72555530197; d2admin-1.25.0-token=702d81e6-b25d-402c-aa22-8560cb66ed92',
   'Authorization': '702d81e6-b25d-402c-aa22-8560cb66ed92',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Host': 'ops-dms-backend.hltn.com',
   'Connection': 'keep-alive'
}
conn.request("POST", "/query/v1/query", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
