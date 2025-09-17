import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# 1. 只认 TLS 1.2 的上下文
ctx = ssl.create_default_context()
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.maximum_version = ssl.TLSVersion.TLSv1_2

# 2. 适配器
class Tls12Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# 3. 请求参数
url = 'https://ops-dms-backend.hltn.com/query/v1/query'
payload = {
    "db_name": "db_course",
    "sql": "select course_id,level,unit,selected_unitmask,teacher_id from main_class_ext where class_course_id = 792 and start_time = 1760007600000 and classroom_status <> -1 limit 100;",
    "limit": 100
}
headers = {
    'Authorization': '702d81e6-b25d-...',
    'Content-Type': 'application/json'
}

# 4. 发请求
with requests.Session() as s:
    s.mount('https://', Tls12Adapter())
    resp = s.post(url, json=payload, headers=headers, timeout=15)
    print(resp.status_code, resp.text)