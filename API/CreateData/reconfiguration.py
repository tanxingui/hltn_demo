#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2024/01/30 15:01
# @Author : 新贵大人
描述: 学员订单推送工具（优化版：提升运行速度）
"""
import base64
import json
import logging
import os
import re
import time
import concurrent.futures
from datetime import datetime, timedelta

import jsonpath
import requests
import openpyxl
from qcloud_cos import CosConfig, CosS3Client


class PushStudentOrder:
    def __init__(self):
        self.subject = self.subject_name()
        self.environment = self.input_environment()
        self.custom_number = self.custom_phone_number()
        self.num = self.input_num() if self.custom_number == "0" else len(self.custom_number)
        self.token = self.get_crm_login_token()
        self.front_sign_data = None  # 缓存Sign数据
        self.cached_phone_list = None  # 缓存手机号列表
        self.importNum = None  # 缓存益智导入编号
        self.excel_paths = {}  # 缓存Excel文件路径

    def get_base64(self, passwd):
        """密码Base64加密"""
        return base64.b64encode(passwd.encode()).decode('utf-8')

    def subject_name(self) -> list:
        """选择学科"""
        while True:
            try:
                choice = int(input("请输入：(1)表达 (2)益智 (3)围棋 (4)数学 (5)魔力耳朵 (6)魔力剑桥 (7)所有学科-->"))
                if 1 <= choice <= 7:
                    all_subjects = ["表达", "益智", "围棋", "数学", "魔力耳朵", "魔力剑桥"]
                    return all_subjects if choice == 7 else [all_subjects[choice - 1]]
                print("请输入1~7之间的数字")
            except ValueError:
                print("输入错误，请输入数字")

    def custom_phone_number(self):
        """输入自定义手机号"""
        while True:
            custom_number = input("请输入：你需要导单的手机号(用逗号隔开)，输入0则不需要自定义-->")
            if custom_number == "0":
                return "0"
            elif not custom_number:
                return "0"

            # 统一分隔符并清洗手机号
            custom_number = re.sub(r'[，.、。\s]+', ',', custom_number)
            phone_numbers = [phone.strip() for phone in custom_number.split(',') if phone.strip()]

            # 简单校验手机号格式（11位数字）
            if all(len(phone) == 11 and phone.isdigit() for phone in phone_numbers):
                return phone_numbers
            print("请输入11位数字的手机号，多个用逗号分隔")

    def input_environment(self):
        """选择环境（魔力耳朵固定UAT）"""
        if "魔力耳朵" in self.subject:
            return "uat"

        while True:
            try:
                environment = int(input("请输入：(1)测试环境  (2)预发布环境-->"))
                return "uat" if environment == 1 else "preprod" if environment == 2 else None
            except ValueError:
                print("输入错误，请输入数字1或2")

    def input_num(self):
        """输入订单条数（1-100）"""
        while True:
            try:
                num = int(input(f"请输入：{self.environment}环境需要导入的订单条数-->"))
                if 0 < num <= 100:
                    return num
                print("请输入1~100之间的数字")
            except ValueError:
                print("输入错误，请输入数字")

    def handle_api_response(self, response):
        """统一处理API响应"""
        try:
            response.raise_for_status()
            resp_json = response.json()
            # 兼容不同API的成功标识
            if resp_json.get('code') in (0, 200) or resp_json.get('success') == "true":
                return resp_json
            return {"error": f"API响应错误: {resp_json.get('msg', resp_json.get('message', '未知错误'))}"}
        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
            return {"error": f"请求失败: {str(e)}"}

    def get_excel_file_path(self, file_name):
        """获取Excel路径（缓存避免重复计算）"""
        if file_name in self.excel_paths:
            return self.excel_paths[file_name]

        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, f"{file_name}.xlsx")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Excel文件不存在：{file_path}")

        self.excel_paths[file_name] = file_path
        return file_path

    def get_crm_login_token(self, username=18707699952, passw='klzz1234@@'):
        """获取CRM登录Token（仅初始化时调用1次）"""
        url = f'https://{self.environment}-auth-new.vipthink.cn/iam-sso/v2/auth/admin/token'
        data = {
            "account": username,
            "password": self.get_base64(passw),
            "loginType": "acc_pwd"
        }
        resp = self.handle_api_response(requests.post(url, json=data))
        if resp.get('code') == 0:
            return resp.get('data', {}).get('token', '')
        print("CRM登录失败，无法获取Token")
        return ""

    def _generate_new_phones(self, count):
        """生成新手机号（用时间戳保证唯一性）"""
        new_phones = set()
        while len(new_phones) < count:
            timestamp = str(time.time()).replace('.', '')[-10:]
            new_phones.add(f'1{timestamp}')
        return new_phones

    def _single_phone_check(self, phone):
        """单个手机号校验（供多线程调用）"""
        if not self.token:
            return False

        url = f'https://{self.environment}-gw.vipthink.cn/api/member/v3/back/ol-user/getUserInfoByMobile'
        payload = {"mobile": phone}
        headers = {"authorization": self.token}
        resp = self.handle_api_response(requests.post(url, json=payload, headers=headers))

        # 手机号不存在（可使用）返回True
        return resp and resp.get('code') == 0 and not resp.get('data')

    def _check_existing_phones(self, new_phones):
        """批量校验手机号（多线程并发，提升速度）"""
        phone_list = []
        if not new_phones:
            return phone_list

        # 多线程并发校验（最大10个线程，避免触发API限流）
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_phone = {executor.submit(self._single_phone_check, p): p for p in new_phones}
            for future in concurrent.futures.as_completed(future_to_phone):
                phone = future_to_phone[future]
                try:
                    if future.result():
                        phone_list.append(phone)
                except Exception as e:
                    print(f"校验手机号{phone}失败：{str(e)}")

        return phone_list

    def get_student_phone(self) -> list:
        """获取可用手机号（缓存避免重复生成）"""
        if self.cached_phone_list is not None:
            return self.cached_phone_list

        self.cached_phone_list = []
        # 自定义手机号直接使用
        if self.custom_number != "0":
            self.cached_phone_list = self.custom_number
            return self.cached_phone_list

        # 生成并校验手机号（直到满足所需数量）
        needed_count = self.num
        while len(self.cached_phone_list) < needed_count:
            # 生成比需要多20%的手机号，应对重复/已存在情况
            generate_count = needed_count - len(self.cached_phone_list) + int(needed_count * 0.2)
            new_phones = self._generate_new_phones(generate_count)
            valid_phones = self._check_existing_phones(new_phones)
            self.cached_phone_list.extend(valid_phones)

        # 截取所需数量（避免超出）
        self.cached_phone_list = self.cached_phone_list[:needed_count]
        return self.cached_phone_list

    def operation_table(self):
        """批量处理Excel（减少IO操作，提升速度）"""
        data_list = self.get_student_phone()
        if not data_list:
            print("无可用手机号，无法生成Excel数据")
            return

        # 统一生成时间格式（避免重复计算）
        yesterday = datetime.now() - timedelta(days=1)
        formatted_datetime1 = yesterday.strftime("%Y-%m-%d %H:%M:%S")  # 支付时间格式
        formatted_datetime2 = yesterday.strftime("%Y%m%d%H%M%S")  # 订单号时间格式

        # 环境配置（按学科区分参数）
        environment_settings = {
            "uat": {
                "表达": {"skuId": "31827746", "amount": "20.01", "file": "biaoda", "sheet": "Sheet1"},
                "围棋": {"skuId": "31828570", "amount": "0.01", "file": "biaoda", "sheet": "Sheet1"},
                "数学": {"skuId": "31835572", "amount": "0.02", "file": "biaoda", "sheet": "Sheet1"},
                "魔力耳朵": {"skuId": "31832911", "amount": "500", "file": "biaoda", "sheet": "Sheet1"},
                "魔力剑桥": {"skuId": "31832305", "amount": "12.67", "file": "biaoda", "sheet": "Sheet1"},
                "益智": {"skuId": "10026037", "amount": "51", "file": "yizhi", "sheet": "导入主表"}
            },
            "preprod": {
                "表达": {"skuId": "20529443", "amount": "0.01", "file": "biaoda", "sheet": "Sheet1"},
                "围棋": {"skuId": "20529441", "amount": "0.01", "file": "biaoda", "sheet": "Sheet1"},
                "数学": {"skuId": "20536367", "amount": "0.02", "file": "biaoda", "sheet": "Sheet1"},
                "魔力剑桥": {"skuId": "20532903", "amount": "9.99", "file": "biaoda", "sheet": "Sheet1"},
                "益智": {"skuId": "10016747", "amount": "80", "file": "yizhi", "sheet": "导入主表"}
            }
        }

        # 获取当前学科配置
        subject_cfg = environment_settings.get(self.environment, {}).get(self.subject)
        if not subject_cfg:
            print(f"未找到{self.environment}环境{self.subject}学科的配置")
            return

        file_path = self.get_excel_file_path(subject_cfg["file"])
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[subject_cfg["sheet"]]

        # 1. 清空历史数据（一次性删除，避免逐行删）
        if sheet.max_row > 2:
            sheet.delete_rows(3, sheet.max_row - 2)  # 从第3行开始删，保留前2行模板

        # 2. 批量生成数据（按行组织）
        rows_data = []
        for phone in data_list:
            order_no = f'XG{formatted_datetime2}{phone[-6:]}'  # 订单号（取手机号后6位，更短易识别）

            if self.subject == "益智":
                # 益智学科Excel列：外部订单号、姓名、区号、手机号、学员id、渠道id、套餐id、金额、支付时间、支付方式、收款渠道、获得原因、父订单号、空列、是否需要地址
                rows_data.append([
                    order_no, "新贵测试", "86", phone, "", "468078",
                    subject_cfg["skuId"], subject_cfg["amount"], formatted_datetime1,
                    "第三方售卖", "0", "1999", "", "", "0"
                ])
            else:
                # 其他学科Excel列：第三方订单号、收款渠道、空列、区号、手机号、空列、空列、套餐id、金额、支付时间、支付方式、渠道id、获得原因、空列、是否需要地址
                rows_data.append([
                    order_no, "0", "", "86", phone, "", "",
                    subject_cfg["skuId"], subject_cfg["amount"], formatted_datetime1,
                    "free", "0", "1999", "", "0"
                ])

        # 3. 批量写入Excel（一次性append，减少IO）
        for row in rows_data:
            sheet.append(row)

        # 4. 保存关闭（仅1次IO）
        workbook.save(file_path)
        workbook.close()
        print(f"{self.subject}学科Excel生成完成，共{len(rows_data)}条数据")

    def get_front_sign(self):
        """获取COS上传签名（缓存避免重复请求）"""
        if self.front_sign_data is not None:
            return self.front_sign_data

        if not self.token:
            print("无Token，无法获取COS签名")
            return {}

        url = f'https://{self.environment}-attch-api.vipthink.cn/v1/attach/getSign'
        data = {
            "name": "biaoda.xlsx",
            "dir": "uploads/images",
            "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "ext": "xlsx",
            "size": 16243,
            "driver": "tencent_oss",
            "code": "platform-trade"
        }
        headers = {"authorization": self.token}
        resp = self.handle_api_response(requests.post(url, json=data, headers=headers))

        if resp and "data" in resp:
            data_dict = resp["data"]
            self.front_sign_data = {
                "id": data_dict.get("id", ""),
                "ossDomain": data_dict.get("ossDomain", ""),
                "path": data_dict.get("path", ""),
                "ossToken": data_dict.get("ossToken", "")
            }

        return self.front_sign_data

    def update_file_to_cos(self):
        """上传Excel到COS（复用缓存的Sign数据）"""
        self.operation_table()
        front_sign = self.get_front_sign()
        if not (front_sign and front_sign.get("ossToken")):
            print("COS签名获取失败，无法上传文件")
            return None

        # 解析COS临时密钥
        try:
            oss_token = json.loads(front_sign["ossToken"])
            secret_id = oss_token["credentials"]["tmpSecretId"]
            secret_key = oss_token["credentials"]["tmpSecretKey"]
            session_token = oss_token["credentials"]["sessionToken"]
        except json.JSONDecodeError as e:
            print(f"解析COS Token失败：{str(e)}")
            return None

        # 初始化COS客户端
        cos_config = CosConfig(
            Region="ap-guangzhou",
            SecretId=secret_id,
            SecretKey=secret_key,
            Token=session_token,
            Domain=f"test-1253622427.cos.accelerate.myqcloud.com"
        )
        cos_client = CosS3Client(cos_config)

        # 上传文件
        file_path = self.get_excel_file_path("biaoda")
        try:
            with open(file_path, "rb") as fp:
                response = cos_client.put_object(
                    Bucket="test-1253622427",
                    Body=fp,
                    Key=front_sign["path"],
                    StorageClass="STANDARD",
                    ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            print(f"文件上传COS成功，ETag：{response['ETag']}")
            return front_sign
        except Exception as e:
            print(f"上传COS失败：{str(e)}")
            return None

    def import_order(self):
        """非益智学科订单导入"""
        front_sign = self.update_file_to_cos()
        if not front_sign:
            return

        # 1. 通知文件上传完成
        notify_url = f'https://{self.environment}-attch-api.vipthink.cn/v1/attach/notify'
        notify_data = {"id": front_sign["id"], "status": 1}
        notify_resp = self.handle_api_response(
            requests.post(notify_url, json=notify_data, headers={"authorization": self.token})
        )
        if notify_resp.get("error"):
            print(f"通知文件上传状态失败：{notify_resp['error']}")
            return

        # 2. 导入订单
        import_url = f'https://{self.environment}-gw.vipthink.cn/api/trade_order/v1/admin/orderImport/urlImport'
        import_data = {
            "fileUrl": f"{front_sign['ossDomain']}{front_sign['path']}",
            "fileName": "biaoda.xlsx",
            "operatorId": 667508,
            "operatorName": "谭新贵",
            "importType": 1
        }
        import_resp = self.handle_api_response(
            requests.post(import_url, json=import_data, headers={"authorization": self.token})
        )

        # 3. 处理导入结果
        if import_resp.get("error"):
            print(f"订单导入失败：{import_resp['error']}")
            return

        # 检查是否有失败数据
        fail_details = jsonpath.jsonpath(import_resp, "$..importFailDtls")
        if fail_details and fail_details[0]:
            for detail in fail_details[0]:
                print(f"导入失败 - 手机号：{detail['mobile']}，原因：{detail['failReason']}")
        else:
            print(f"{self.subject}学科订单导入成功")

    @property
    def get_batch(self):
        """获取最近2分钟内的导入批次号"""
        if not self.token:
            return ""

        url = f'https://{self.environment}-gw.vipthink.cn/api/trade_order/v1/admin/orderImport/importRecord/list'
        data = {"pageNo": 1, "pageSize": 10}
        resp = self.handle_api_response(
            requests.post(url, json=data, headers={"authorization": self.token})
        )

        if resp.get("error") or not resp.get("data"):
            print("获取批次号失败：无导入记录")
            return ""

        # 筛选2分钟内的“biaoda.xlsx”导入记录
        two_min_ago = datetime.now() - timedelta(minutes=2)
        for record in resp["data"]:
            if record.get("fileName") != "biaoda.xlsx":
                continue

            try:
                create_time = datetime.strptime(record["createTime"], "%Y-%m-%d %H:%M:%S")
                if create_time >= two_min_ago:
                    return record["batchNum"]
            except ValueError:
                continue

        print("未找到最近2分钟内的有效批次号")
        return ""

    def get_order_recordDtlId(self) -> list:
        """获取待审批订单ID列表"""
        batch_num = self.get_batch
        if not batch_num:
            return []

        url = f'https://{self.environment}-gw.vipthink.cn/api/trade_order/v1/admin/orderImport/importRecord/dtlList'
        data = {
            "pageNo": 1,
            "pageSize": 100,
            "batchNum": batch_num,
            "status": "WAIT_APPROVAL"
        }
        resp = self.handle_api_response(
            requests.post(url, json=data, headers={"authorization": self.token})
        )

        if resp.get("error") or not resp.get("data"):
            print("获取待审批订单ID失败")
            return []

        return [item["recordDtlId"] for item in resp["data"]]

    def last_auditing_order(self):
        """非益智学科订单审批"""
        record_dtl_ids = self.get_order_recordDtlId()
        if not record_dtl_ids:
            return

        audit_url = f'https://{self.environment}-gw.vipthink.cn/api/trade_order/v1/admin/orderImport/importRecord/auditDtls'
        headers = {"authorization": self.token}
        batch_num = self.get_batch

        # 批量审批（减少请求次数，每次最多20个ID）
        for i in range(0, len(record_dtl_ids), 20):
            batch_ids = record_dtl_ids[i:i + 20]
            audit_data = {
                "recordDtlIds": batch_ids,
                "batchNum": batch_num,
                "auditStatus": "APPROVAL_SUCCESS",
                "remarks": "测试数据"
            }
            resp = self.handle_api_response(requests.post(audit_url, json=audit_data, headers=headers))

            if resp.get("error"):
                print(f"审批订单ID {batch_ids} 失败：{resp['error']}")
            else:
                order_nums = jsonpath.jsonpath(resp, "$..orderNumber") or []
                print(f"审批成功 - 订单号：{order_nums}")

    def yizhi_order_importNum(self):
        """益智学科获取导入编号（缓存避免重复请求）"""
        if self.importNum is not None:
            return self.importNum

        self.operation_table()
        url = f'https://{self.environment}-order.vipthink.cn/order/v1/order/import'
        file_path = self.get_excel_file_path("yizhi")

        # 上传Excel
        with open(file_path, "rb") as f:
            files = {"file": ("yizhi.xlsx", f)}
            resp = self.handle_api_response(
                requests.post(url, files=files, headers={"authorization": self.token})
            )

        if resp.get("code") == 0 and resp.get("data"):
            self.importNum = resp["data"]["importNum"]
            print(f"益智学科导入成功，导入编号：{self.importNum}")
            return self.importNum

        print(f"益智学科导入失败：{resp.get('error', resp.get('message', '未知错误'))}")
        return ""

    def yizhi_order_id(self) -> list:
        """获取益智待审批订单ID"""
        import_num = self.yizhi_order_importNum()
        if not import_num:
            return []

        # 1. 进入待审核状态
        confirm_url = f"https://{self.environment}-order.vipthink.cn/order/v1/order/orderConfirm"
        confirm_data = {"explainContent": "测试一下", "importNum": import_num}
        confirm_resp = self.handle_api_response(
            requests.post(confirm_url, json=confirm_data, headers={"authorization": self.token})
        )
        if confirm_resp.get("error"):
            print(f"益智订单进入待审核失败：{confirm_resp['error']}")
            return []

        # 2. 获取待审批ID
        list_url = f"https://{self.environment}-order.vipthink.cn/order/v1/order/importDetailList"
        list_data = {"status": 1, "page": 1, "limit": 100, "importNum": import_num}
        list_resp = self.handle_api_response(
            requests.post(list_url, json=list_data, headers={"authorization": self.token})
        )

        if list_resp.get("code") != 0 or not list_resp.get("data", {}).get("data"):
            print("获取益智待审批订单ID失败")
            return []

        return [item["id"] for item in list_resp["data"]["data"]]

    def yizhi_last_audit(self):
        """益智学科订单审批"""
        order_ids = self.yizhi_order_id()
        if not order_ids:
            return

        audit_url = f"https://{self.environment}-order.vipthink.cn/order/v1/order/handleMetadata"
        audit_data = {
            "handleType": 1,
            "metadataIdList": order_ids,
            "importNum": self.importNum
        }
        resp = self.handle_api_response(
            requests.post(audit_url, json=audit_data, headers={"authorization": self.token})
        )

        if resp.get("code") == 0:
            print(f"益智学科订单审批成功，共{len(order_ids)}条")
        else:
            print(f"益智学科订单审批失败：{resp.get('error', resp.get('message', '未知错误'))}")

    def get_student_account(self):
        """获取学员账户信息（多线程提升速度）"""
        phone_list = self.get_student_phone()
        if not phone_list:
            return

        print("\n学员账户信息：")
        print("-" * 60)
        print(f"{'大账户ID':<20} {'豌豆ID':<20} {'手机号':<15}")
        print("-" * 60)

        # 多线程并发查询
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_phone = {executor.submit(self._get_single_account, p): p for p in phone_list}
            for future in concurrent.futures.as_completed(future_to_phone):
                phone = future_to_phone[future]
                try:
                    unification_id, user_id = future.result()
                    print(f"{unification_id:<20} {user_id:<20} {phone:<15}")
                except Exception as e:
                    print(f"获取手机号{phone}信息失败：{str(e)}")
        print("-" * 60)

    def _get_single_account(self, phone):
        """单个学员账户查询（供多线程调用）"""
        url = f'https://{self.environment}-gw.vipthink.cn/api/member/v3/back/ol-user/getUserInfoByMobile'
        payload = {"mobile": phone}
        headers = {"authorization": self.token}
        resp = self.handle_api_response(requests.post(url, json=payload, headers=headers))

        if resp.get("code") != 0 or not resp.get("data"):
            raise Exception("未查询到账户信息")

        data = resp["data"][0]
        return data.get("unificationId", ""), data.get("userId", "")

    def main(self):
        """主执行函数（按学科批量处理）"""
        if not self.token:
            print("未获取到登录Token，程序终止")
            return

        print(f"\n开始处理【{self.environment}环境】【{','.join(self.subject)}】学科订单")
        print(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        for subject in self.subject:
            self.subject = subject  # 切换当前处理的学科
            print(f"\n正在处理【{subject}】学科...")

            try:
                if subject in ("表达", "围棋", "数学", "魔力耳朵", "魔力剑桥"):
                    self.import_order()  # 导入订单
                    self.last_auditing_order()  # 审批订单
                elif subject == "益智":
                    self.yizhi_last_audit()  # 益智导入+审批一体化
                else:
                    print(f"未支持的学科：{subject}")
                    continue

                # 获取学员账户信息（所有学科处理完后统一查询，减少重复）
                if subject == self.subject[-1]:
                    self.get_student_account()

            except Exception as e:
                print(f"处理【{subject}】学科异常：{str(e)}")
                continue

        print(f"\n所有学科处理完成！")
        print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    # 初始化日志（便于排查问题）
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    # 启动程序
    try:
        RunPushStudentOrder = PushStudentOrder()
        RunPushStudentOrder.main()
    except KeyboardInterrupt:
        print("\n程序被手动终止")
    except Exception as e:
        print(f"程序初始化失败：{str(e)}")