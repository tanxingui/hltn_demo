import aiohttp
import asyncio

ip = "10.4.130.252"
#
# # 接口地址（请补充完整域名）
# API_URL = f"http://{ip}:8080/course/parent/targetClass"
#
# # 两组请求参数
# PARAMS_LIST = [
#     {
#         "live_ids": [
#             22559777
#         ],
#         "type": 1,
#         "original_class_id": 273735,
#         "student_id": 2095618912,
#         "start_time": "2025-10-19 00:00:00",
#         "end_time": "2025-10-28 23:59:59",
#         "time": "09:00-21:00"
#     },
#     {
#         "live_ids": [
#             22559612
#         ],
#         "type": 1,
#         "original_class_id": 273732,
#         "student_id": 2095626599,
#         "start_time": "2025-10-19 00:00:00",
#         "end_time": "2025-10-28 23:59:59",
#         "time": "09:00-21:00"
#     }
# ]
#
# async def async_request(session, url, params):
#     """异步发送POST请求"""
#     try:
#         async with session.post(url, json=params) as response:
#             result = await response.json()
#             print(f"请求成功（student_id: {params['student_id']}）,结果:{result}")
#     except Exception as e:
#         print(f"请求失败（student_id: {params['student_id']}）: {str(e)}\n")
#         return {"error": str(e)}
#
# async def main():
#     """异步主函数"""
#     async with aiohttp.ClientSession() as session:
#         tasks = [async_request(session, API_URL, params) for params in PARAMS_LIST]
#         results = await asyncio.gather(*tasks)
#         return results
#
# if __name__ == "__main__":
#     # 使用 Python 3.7+ 推荐的 asyncio.run() 运行异步代码
#     results = asyncio.run(main())
#     print("所有请求处理完成")



# 调课
# # 接口地址（请补充完整域名）
# API_URL = f"http://{ip}:8080/course/parent/adjustClass"
#
# # 两组请求参数
# PARAMS_LIST = [
#     {
#         "original_class_id": "273735",
#         "student_id": 2095618912,
#         "subject": 11,
#         "original_live_ids": [
#             22559777
#         ],
#         "new_class_id": "273744",
#         "new_live_ids": [
#             22559938
#         ]
#     },
#     {
#         "original_class_id": "273732",
#         "student_id": 2095626599,
#         "subject": 11,
#         "original_live_ids": [
#             22559612
#         ],
#         "new_class_id": "273744",
#         "new_live_ids": [
#             22559938
#         ]
#     }
# ]
#
# async def async_request(session, url, params):
#     """异步发送POST请求"""
#     try:
#         async with session.post(url, json=params) as response:
#             result = await response.json()
#             print(f"请求成功（student_id: {params['student_id']}）,结果:{result}")
#     except Exception as e:
#         print(f"请求失败（student_id: {params['student_id']}）: {str(e)}\n")
#         return {"error": str(e)}
#
# async def main():
#     """异步主函数"""
#     async with aiohttp.ClientSession() as session:
#         tasks = [async_request(session, API_URL, params) for params in PARAMS_LIST]
#         results = await asyncio.gather(*tasks)
#         return results
#
# if __name__ == "__main__":
#     # 使用 Python 3.7+ 推荐的 asyncio.run() 运行异步代码
#     results = asyncio.run(main())
#     print("所有请求处理完成")



#取消调课
# 接口地址（请补充完整域名）
API_URL = f"http://{ip}:8080/course/parent/cancelAdjustClass"

# 两组请求参数
PARAMS_LIST = [
    {
        "record_id": 105
    }
    ,
    {
        "record_id": 106
    }
]

async def async_request(session, url, params):
    """异步发送POST请求"""
    try:
        async with session.post(url, json=params) as response:
            result = await response.json()
            print(f"请求成功（record_id: {params['record_id']}）,结果:{result}")
    except Exception as e:
        print(f"请求失败（record_id: {params['record_id']}）: {str(e)}\n")
        return {"error": str(e)}

async def main():
    """异步主函数"""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(session, API_URL, params) for params in PARAMS_LIST]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    results = asyncio.run(main())
    print("所有请求处理完成")