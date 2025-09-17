import ast
import json, re, datetime as dt
import pandas as pd

with open(r'C:\Users\92101\Desktop\没有合适外教数据.txt', encoding='utf-8') as f:
    raw_text = f.read()

chunks = re.findall(r'班级 (\d+): 200, (\{.*?\})(?=\s*班级|\s*$)', raw_text, flags=re.S)

first_batch = []
second_batch = []
# second_map = {}

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
        # 第二批只记一次
        second_batch.append((cls_id, all_lessons[first_cambridge_idx]['startTime']))

    # # 第二批去重已经在的数据
    # for item in all_lessons[first_cambridge_idx + 1:]:
    #     if item['bookResult'] == '剑桥没有找到适合外教':
    #         ts = item['startTime']
    #         if cls_id not in second_map:
    #             second_map[cls_id] = set()
    #         if ts not in second_map[cls_id]:
    #             second_map[cls_id].add(ts)

def fmt(ts):
    return dt.datetime.fromtimestamp(ts / 1000).strftime('%a %H:%M').replace('Mon', '周一').replace('Tue',
                                                                                                    '周二').replace(
        'Wed', '周三').replace('Thu', '周四').replace('Fri', '周五').replace('Sat', '周六').replace('Sun', '周日')

def ms2str(ms):
    return pd.to_datetime(ms, unit='ms', utc=True).tz_convert('Asia/Shanghai').strftime('%Y-%m-%d %H:%M:%S')

print('第一批（班级第一次出现且前面无“约课成功”）')
for cid, ts in first_batch:
    print(f'班级：{cid}   没约上任何课程的上课时间：{fmt(ts)}')

print('\n第二批（同一个班级第二次及以后出现）')
second_batch = list(dict.fromkeys(second_batch))
for cid, ts in second_batch:
    print(f'班级：{cid}   没有约上外教的上课时间：{ms2str(ts)}')