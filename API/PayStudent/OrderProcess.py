import time
import requests


class OrderProcessor:
    def __init__(self, api_client, file_handler, user_input):
        self.api_client = api_client
        self.file_handler = file_handler
        self.user_input = user_input

    def import_and_audit_order(self):
        token = self.api_client.token
        phone_number = self.user_input.custom_number
        if phone_number == "0":
            data_list = [phone_number for _ in range(self.user_input.num)]
        else:
            data_list = phone_number
        self.file_handler.operation_table(data_list)
        url = f"https://{self.user_input.environment}-api-backend-customer.vipthink.cn/vipthink-crm-order/v1/ai/order/import"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with open(self.file_handler.get_path('biaoda'), 'rb') as file:
            files = {'file': ('file', file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = self.api_client.handle_api_response(requests.post(url, headers=headers, files=files))
            if response:
                print("文件上传成功！")
                self.check_import_order_data(response['data']['id'])

    def check_import_order_data(self, order_id):
        print(f"导单id是: {order_id}")
        url = f"https://{self.user_input.environment}-api-backend-customer.vipthink.cn/vipthink-crm-order/v1/ai/order/checkImportOrderData"
        data = {"id": order_id}
        headers = {'Authorization': f'Bearer {self.api_client.token}'}
        for _ in range(5):
            response = self.api_client.handle_api_response(requests.post(url, json=data, headers=headers))
            if response and response['data']['status'] == 3:
                print(f"订单导入成功: {response['data']}")
                return
            else:
                time.sleep(10)
        print("订单导入失败，请检查日志或联系管理员。")

    def yizhi_order_import(self):
        token = self.api_client.token
        phone_number = self.user_input.custom_number

        # 生成需要导入的数据列表
        if phone_number == "0":
            data_list = [f"{i + 1:011d}" for i in range(self.user_input.num)]  # 模拟生成自定义数据
        else:
            data_list = phone_number

        # 调用文件处理模块生成文件
        self.file_handler.operation_table(data_list)

        # 上传文件
        url = f"https://{self.user_input.environment}-api-backend-customer.vipthink.cn/vipthink-crm-order/v1/yizhi/order/import"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with open(self.file_handler.get_path('yizhi'), 'rb') as file:
            files = {'file': ('file', file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = self.api_client.handle_api_response(requests.post(url, headers=headers, files=files))
            if response:
                print("文件上传成功！")
                self.check_yizhi_order_import(response['data']['id'])

    def check_yizhi_order_import(self, order_id):
        print(f"导单id是: {order_id}")
        url = f"https://{self.user_input.environment}-api-backend-customer.vipthink.cn/vipthink-crm-order/v1/yizhi/order/checkImportOrderData"
        data = {"id": order_id}
        headers = {'Authorization': f'Bearer {self.api_client.token}'}
        for _ in range(5):
            response = self.api_client.handle_api_response(requests.post(url, json=data, headers=headers))
            if response and response['data']['status'] == 3:
                print(f"订单导入成功: {response['data']}")
                return
            else:
                time.sleep(10)
        print("订单导入失败，请检查日志或联系管理员。")
