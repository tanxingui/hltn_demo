#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
描述: 比较旧接口和新接口的返回结果差异
"""

import pymysql
import requests
import re
from interface_params import get_params_by_id

# 数据库连接配置
DB_CONFIG = {
    'host': '10.4.32.47',
    'port': 3306,
    'user': 'shdev',
    'passwd': '6JrpIH4DbtE1w2YH',
    'db': 'ems'
}

# 默认请求头
Token = {
    'authorization': 'Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.W3sibmJmIjoxNzc2MjIzOTI0LCJpc3MiOiJkb2YiLCJ0emEiOiJDU1QiLCJleHAiOjE3NzYzMTAzMjQsImlhdCI6MTc3NjIyMzkyNCwic2lkIjoxfSx7InJhbmQiOiI5ODk5MzkzMDQ2OTI2NTQzNDI4MzcxNTg1NzQwMDY4MDM0ODU5MDgzNzU0MDEzNDA5MDIxNjM0MDA2Mjk0NzM3IiwidWlkIjo2Njc1MDgsInR5cCI6ImEiLCJ0aW1lIjoxNzc2MjIzOTI0fV0.OWZhZDkyNWY1NWFiYmQ2MzM2MDljMDUxNWJjOTcyZDJiMzJlNGIzY2VkNWUyZGVkZGQ4NzdjMjYwYzdhZjcxMg'
}

def get_db_data(interface_id):
    """根据id获取数据库中的接口配置数据"""
    try:
        # 连接数据库
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # 执行查询
                sql = "SELECT path, rewrite FROM ems.ol_ems_interface_config WHERE id = %s"
                cursor.execute(sql, (interface_id,))
                return cursor.fetchone()
    except Exception as e:
        print(f"数据库操作错误: {e}")
        return None

def call_api(method, url, headers, params):
    """调用API并返回响应结果"""
    try:
        method = method.upper()
        # 处理NO_PARAMS_SPECIAL_FLAG
        if params == "NO_PARAMS_SPECIAL_FLAG":
            params = None
        if method == 'GET':
            response = requests.get(
                url, 
                headers=headers, 
                params=params if params else None, 
                timeout=30
            )
        elif method == 'POST':
            response = requests.post(
                url, 
                headers=headers, 
                json=params if params else None, 
                timeout=30
            )
        else:
            print(f"不支持的请求方式: {method}")
            return None
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except Exception as e:
        print(f"调用接口失败: {url}, 错误: {e}")
        return None

def compare_results(old_result, new_result):
    """比较两个接口的返回结果并输出差异"""
    differences = []
    diff_count = 1
    processed_diffs = set()  # 用于记录已处理过的差异类型
    excluded_keys = {'msg', 'time', 'traceId', '__log__'}  # 不需要打印的字段

    def compare_recursive(old, new, current_path=""):
        nonlocal diff_count

        # 处理类型不同的情况
        if type(old) != type(new):
            # 提取字段名（去掉列表索引，获取最后一个字段名），确保每个字段只显示一次类型差异
            field_path = re.sub(r'\[\d+\]', '', current_path)  # 去掉所有 [数字]
            field_name = field_path.split('.')[-1] if '.' in field_path else field_path
            diff_key = f"type_{field_name}"
            if diff_key not in processed_diffs:
                differences.append(
                    f"{diff_count}. 字段: {current_path}, 类型不同 - 旧接口: {type(old).__name__}, 新接口: {type(new).__name__}"
                )
                diff_count += 1
                processed_diffs.add(diff_key)
            return

        # 处理字典类型
        if isinstance(old, dict):
            # 检查旧接口有但新接口没有的键
            for key in old:
                if key not in new:
                    # 跳过不需要打印的字段
                    if key in excluded_keys:
                        continue
                    diff_key = f"missing_key_{key}"
                    if diff_key not in processed_diffs:
                        differences.append(
                            f"{diff_count}. 字段: {current_path}.{key}, 键缺失 - 旧接口有该键，新接口没有"
                        )
                        diff_count += 1
                        processed_diffs.add(diff_key)
                else:
                    compare_recursive(
                        old[key],
                        new[key],
                        f"{current_path}.{key}" if current_path else key
                    )
            # 检查新接口有但旧接口没有的键
            for key in new:
                if key not in old:
                    diff_key = f"new_key_{key}"
                    if diff_key not in processed_diffs:
                        differences.append(
                            f"{diff_count}. 字段: {current_path}.{key}, 键新增 - 新接口有该键，旧接口没有"
                        )
                        diff_count += 1
                        processed_diffs.add(diff_key)
        # 处理列表类型
        elif isinstance(old, list):
            min_length = min(len(old), len(new))
            # 比较共同部分
            for i in range(min_length):
                compare_recursive(
                    old[i],
                    new[i],
                    f"{current_path}[{i}]" if current_path else f"[{i}]"
                )
            # 检查长度差异
            if len(old) != len(new):
                diff_key = f"list_length_{current_path}"
                if diff_key not in processed_diffs:
                    differences.append(
                        f"{diff_count}. 字段: {current_path}, 列表长度不同 - 旧接口长度: {len(old)}, 新接口长度: {len(new)}"
                    )
                    diff_count += 1
                    processed_diffs.add(diff_key)
        # 处理基本类型
        else:
            if old != new:
                # 提取字段名（去掉列表索引，获取最后一个字段名），确保每个字段只显示一次差异
                # 对于 data[0].basisName，先去掉 [0] 等列表索引，再取最后一个字段名
                field_path = re.sub(r'\[\d+\]', '', current_path)  # 去掉所有 [数字]
                field_name = field_path.split('.')[-1] if '.' in field_path else field_path
                
                # 调试信息：打印字段差异详情
                print(f"\n发现值差异 - 路径: {current_path},   字段名: {field_name}")
                print(f"[DEBUG] 旧值: {old} (类型: {type(old).__name__}), 新值: {new} (类型: {type(new).__name__})")
                
                if field_name not in processed_diffs:
                    differences.append(
                        f"{diff_count}. 字段: {current_path}, 值不同 - 旧接口: {old}, 新接口: {new}"
                    )
                    diff_count += 1
                    processed_diffs.add(field_name)
                    print(f"结果 --> 已添加到差异列表")
                else:
                    print(f"结果 --> 已跳过（该字段已处理过）")

    compare_recursive(old_result, new_result)
    return differences

def compare_apis(method, interface_id, params=None):
    """比较新旧接口的返回结果差异
    
    Args:
        method: 请求方式，如 'get' 或 'post'
        interface_id: ol_ems_interface_config表的id
        params: 接口参数，字典格式，可选（不传则根据interface_id自动查找，未找到则不传参）
        
    Returns:
        differences: 差异列表
    """
    # 1. 连接数据库查询接口配置
    db_result = get_db_data(interface_id)

    if not db_result:
        print("未查询到接口配置数据")
        return []

    # 2. 获取接口路径
    old_url, new_url = db_result
    if not old_url or not new_url:
        print("接口路径为空，无法比较")
        return []

    # 我一般会在接口后面加个1，然后再系统就会获取旧的接口，这里是根据我自己的习惯去掉1
    if old_url[-1] == '1':
        old_url = old_url[:-1]

    # 3. 获取请求参数（优先使用传入的params，否则根据ID自动查找）
    if params is None:
        params = get_params_by_id(interface_id)

    # 4. 打印比较信息
    print(f"比较接口: 旧：{old_url} vs 新：{new_url}")
    print(f"请求方式: {method}")
    print(f"使用参数: {params if params else '无'}")

    # 5. 调用接口
    old_result = call_api(method, old_url, Token, params)
    new_result = call_api(method, new_url, Token, params)

    if old_result is None or new_result is None:
        print("接口调用失败，跳过比较")
        return []

    # 5. 比较结果
    differences = compare_results(old_result, new_result)

    if differences:
        print("\n最终结果，发现以下差异:")
        for diff in differences:
            print(diff)
    else:
        print("两个接口返回结果一致，无差异")
    
    return differences

if __name__ == '__main__':
    # 根据接口ID自动查找参数（从 interface_params.py 中获取）
    compare_apis("post", "8")