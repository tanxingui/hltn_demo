# 操作需要上传的表格
from datetime import datetime
import openpyxl
from PaidStudent import PushStudentOrder

class ExcelDatabase:
    def __init__(self):
        self.subject = self.subject()
        self.environment = self.input_environment()
        
    def subject(self):
        while True:
            subject = input("请输入：(1)-->口才    (2)-->益智")
            try:
                subject = int(subject)
            except ValueError:
                print("输入错误，请输入数字")
                continue
            if subject == 1:
                return "口才"
            elif subject == 2:
                return "益智"
            else:
                print("请输入一个数字(1)/(2)获取正确的学科")
                continue

    def input_environment(self):
        while True:
            environment = input("请输入：(1)-->测试环境    (2)-->预发布环境")
            try:
                environment = int(environment)
            except ValueError:
                print("输入错误，请输入数字")
                continue
            if environment == 1:
                return "uat"
            elif environment == 2:
                return "preprod"
            else:
                print("请输入一个数字(1)/(2)获取正确的环境")
                continue

    def operation_table(self):
        '''

        :param identification: 为Flase的时候，可以自定义手机号导单
        :return:
        '''
        data_list = PushStudentOrder().get_student_phone()
        formatted_datetime1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_datetime2 = datetime.now().strftime("%Y%m%d%H%M%S")
        if self.subject == "口才":
            file_path = self.get_path('test')
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook["Sheet1"]
            # 清空表格的数据
            if sheet.max_row > 2:
                # 行号是从1开始计数的，而不是从0开始，所以这里是3，
                for row in range(3, sheet.max_row + 1):
                    sheet.delete_rows(row)
            if self.environment == "uat":
                for index, value in enumerate(data_list):
                    sheet.cell(row=3 + index, column=2, value='0')  # 收款渠道
                    sheet.cell(row=3 + index, column=4, value="86")  # 手机区号
                    sheet.cell(row=3 + index, column=8, value='31825515')  # 套餐skuid
                    sheet.cell(row=3 + index, column=9, value='0.02')  # 订单支付金额
                    sheet.cell(row=3 + index, column=10, value=formatted_datetime1)  # 支付时间
                    sheet.cell(row=3 + index, column=11, value="free")  # 支付方式
                    sheet.cell(row=3 + index, column=12, value="0")  # 渠道id
                    sheet.cell(row=3 + index, column=13, value="1999")  # 获得原因
                    sheet.cell(row=3 + index, column=15, value="0")  # 是否需要地址
                    sheet.cell(row=3 + index, column=1, value=f'XG{formatted_datetime2}{value}')  # 第三方订单号
                    sheet.cell(row=3 + index, column=5, value=value)  # 手机号
            elif self.environment == "preprod":
                for index, value in enumerate(data_list):
                    sheet.cell(row=3 + index, column=2, value='0')  # 收款渠道
                    sheet.cell(row=3 + index, column=4, value="86")  # 手机区号
                    sheet.cell(row=3 + index, column=8, value='20528464')  # 套餐skuid
                    sheet.cell(row=3 + index, column=9, value='0.01')  # 订单支付金额
                    sheet.cell(row=3 + index, column=10, value=formatted_datetime1)  # 支付时间
                    sheet.cell(row=3 + index, column=11, value="free")  # 支付方式
                    sheet.cell(row=3 + index, column=12, value="0")  # 渠道id
                    sheet.cell(row=3 + index, column=13, value="1999")  # 获得原因
                    sheet.cell(row=3 + index, column=15, value="0")  # 是否需要地址
                    sheet.cell(row=3 + index, column=1, value=f'XG{formatted_datetime2}{value}')  # 第三方订单号
                    sheet.cell(row=3 + index, column=5, value=value)  # 手机号
            workbook.save(file_path)
            workbook.close()
        elif self.subject == "益智":
            file_path = self.get_path('yizhi')
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook["导入主表"]
            # 清空表格的数据
            if sheet.max_row > 2:
                # 行号是从1开始计数的，而不是从0开始，所以这里是3，
                for row in range(3, sheet.max_row + 1):
                    sheet.delete_rows(row)
            if self.environment == "uat":
                for index, value in enumerate(data_list):
                    sheet.cell(row=3 + index, column=2, value='新贵测试')  # 用户姓名
                    sheet.cell(row=3 + index, column=3, value="86")  # 手机区号
                    sheet.cell(row=3 + index, column=5, value='')  # 学员id
                    sheet.cell(row=3 + index, column=6, value='468078')  # 渠道id
                    sheet.cell(row=3 + index, column=7, value='10025667')  # 套餐id
                    sheet.cell(row=3 + index, column=8, value="0.03")  # 订单支付金额
                    sheet.cell(row=3 + index, column=9, value=formatted_datetime1)  # 支付时间
                    sheet.cell(row=3 + index, column=10, value="第三方售卖")  # 支付方式
                    sheet.cell(row=3 + index, column=11, value="0")  # 收款渠道id
                    sheet.cell(row=3 + index, column=12, value="1999")  # 获得原因
                    sheet.cell(row=3 + index, column=13, value="")  # 父订单号
                    sheet.cell(row=3 + index, column=15, value="0")  # 是否需要地址
                    sheet.cell(row=3 + index, column=1, value=f'XG{formatted_datetime2}{value}')  # 外部订单号
                    sheet.cell(row=3 + index, column=4, value=value)  # 手机号
            elif self.environment == "preprod":
                for index, value in enumerate(data_list):
                    sheet.cell(row=3 + index, column=2, value='新贵测试')  # 用户姓名
                    sheet.cell(row=3 + index, column=3, value="86")  # 手机区号
                    sheet.cell(row=3 + index, column=5, value='')  # 学员id
                    sheet.cell(row=3 + index, column=6, value='470640')  # 渠道id
                    sheet.cell(row=3 + index, column=7, value='10016610')  # 套餐id
                    sheet.cell(row=3 + index, column=8, value="0.01")  # 订单支付金额
                    sheet.cell(row=3 + index, column=9, value=formatted_datetime1)  # 支付时间
                    sheet.cell(row=3 + index, column=10, value="第三方售卖")  # 支付方式
                    sheet.cell(row=3 + index, column=11, value="0")  # 收款渠道id
                    sheet.cell(row=3 + index, column=12, value="1999")  # 获得原因
                    sheet.cell(row=3 + index, column=13, value="")  # 父订单号
                    sheet.cell(row=3 + index, column=15, value="0")  # 是否需要地址
                    sheet.cell(row=3 + index, column=1, value=f'XG{formatted_datetime2}{value}')  # 外部订单号
                    sheet.cell(row=3 + index, column=4, value=value)  # 手机号
            workbook.save(file_path)
            workbook.close()