#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/06/28 18:10
# @Author : 新贵大人
描述:
"""
from PayStudent.ApiInteractions import APIClient
from PayStudent.FileOperations import FileHandler
from PayStudent.OrderProcess import OrderProcessor
from PayStudent.UserInput import UserInputHandler


def main():
    user_input = UserInputHandler()
    file_handler = FileHandler(user_input.environment, user_input.subject)
    api_client = APIClient(user_input.environment, user_input.get_crm_login_token(18707699952,"klzz1234@@"))
    order_processor = OrderProcessor(api_client, file_handler, user_input)

    if user_input.subject in ["口才", "魔力"]:
        order_processor.import_and_audit_order()
    elif user_input.subject == "益智":
        order_processor.yizhi_order_import()


if __name__ == '__main__':
    main()
