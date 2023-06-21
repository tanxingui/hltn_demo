# import time
#
# class Decorator(object):
#     def __init__(self, fuc):
#         self.fuc = fuc
#
#     def __call__(self, *args, **kwargs):
#         print(f'{self.fuc.__name__}函数运行前')
#         starttime = time.time()
#         result = self.fuc(*args, **kwargs)
#         endtime = time.time()
#         print(f"{self.fuc.__name__}函数运行后:\n一共用了{(endtime - starttime):.2f}秒")
#         return result
#
# @Decorator
# def demo(x, y):
#     time.sleep(0.2)
#     print(x, y)
#     return x * y
#
#
# if __name__ == '__main__':
#     print(demo(2, 3))




import requests

def auth(f):
    def get_header(*args, **kwargs):
        response = f(*args, **kwargs)
        headers = {'authorization': f'Bearer {response}'}
        return headers
    return get_header

@auth
def login():
    url = 'https://uat-auth.vipthink.cn/v1/auth/admin/token'
    data = {"__fields": "token,uid", "username": '18707699952', "password": 'Klzz1234'}
    response = requests.post(url, json=data)
    print(type(response))
    print(response.headers)
    print(hasattr(response,'headers'))
    return response.json()['data']['token']

# def demo_api():
#     url = 'https://sht-eos-gateway.vipthink.cn/cc-backend/lesson/getLessonList'
#     data = {"uuid": "12131649","subject_id": 1,"page_count": 1,"page_size": 20,"course_id": 5189}
#     response = requests.post(url, json=data,headers=login())
#     print(response.json())

print(login())
# demo_api()

