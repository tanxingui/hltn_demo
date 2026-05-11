#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/06/28 18:12
# @Author : 新贵大人
描述:
"""
import base64
import json
import requests

class APIClient:
    def __init__(self, environment, token):
        self.environment = environment
        self.token = token

    def handle_api_response(self, response):
        try:
            response.raise_for_status()
            resp_json = response.json()
            if resp_json['code'] == 0 or resp_json['code'] == 200 or resp_json['success'] == "true":
                return resp_json
            else:
                return {"error": f"API响应错误: {resp_json['msg']}"}
        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError, KeyError) as e:
            return {"error": f"操作失败！请求错误: {e}"}


    def request_order_id(self, custom_number):
        if not custom_number:
            return None
        url = f'https://{self.environment}-api-backend-customer.vipthink.cn/vipthink-crm-member/v2/student/getPhoneStudentInfo'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = self.handle_api_response(requests.post(url, json={"phone": custom_number}, headers=headers))
        if 'error' not in response:
            return response['data'][0]['id'] if response['data'] else None
        else:
            print(response['error'])
            return None

if __name__ == '__main__':
    APIClient().get_crm_login_token()