import ast
import  re, datetime as dt
import pandas as pd

with open(r'C:\Users\92101\Desktop\没有合适外教数据.txt', encoding='utf-8') as f:
    raw_text = f.read()

chunks = re.findall(r'班级 (\d+): 200, (\{.*?\})(?=\s*班级|\s*$)', raw_text, flags=re.S)

first_batch = []
second_batch = []

for cls_id_str, json_str in chunks:
    cls_id = int(cls_id_str)
    data = ast.literal_eval(json_str)['data']['list']

    # 1. 整理数据，不需要学员
    all_lessons = []
    for stu in data:
        for lesson in stu['list']:
            all_lessons.append(lesson)

    first_cambridge_idx = None
    for idx, item in enumerate(all_lessons):
        if item['bookResult'] == '剑桥没有找到适合外教':
            first_cambridge_idx = idx
            break

    if first_cambridge_idx is None:
        continue

    # 第一批
    if first_cambridge_idx == 0:
        first_batch.append((cls_id, all_lessons[first_cambridge_idx]['startTime']))
    else:
        # 第二批
        second_batch.append((cls_id, all_lessons[first_cambridge_idx]['startTime']))

WEEKDAY_MAP = {'Mon': '周一', 'Tue': '周二', 'Wed': '周三', 'Thu': '周四',  'Fri': '周五', 'Sat': '周六', 'Sun': '周日'}

def ms2str(ms):
    local_dt = pd.to_datetime(ms, unit='ms', utc=True).tz_convert('Asia/Shanghai')
    weekday = WEEKDAY_MAP[dt.datetime.fromtimestamp(ms/1000).strftime('%a')]
    return f"{local_dt.strftime('%Y-%m-%d')} {weekday} {local_dt.strftime('%H:%M:%S')}"

print('第一批')
for cid, ts in first_batch:
    print(f'班级：{cid}   没约上任何课程： {ms2str(ts)}')

print('\n第二批')
second_batch = list(dict.fromkeys(second_batch))
for cid, ts in second_batch:
    print(f'班级：{cid}   班级部分课程没有外教：{ms2str(ts)}')