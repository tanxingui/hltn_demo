#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

print("开始测试数据库连接")

try:
    # 尝试连接数据库
    conn = pymysql.connect(
        host='10.4.32.47',
        port=3306,
        user='shdev',
        passwd='6JrpIH4DbtE1w2YH',
        db='ems'
    )
    print("数据库连接成功")
    
    # 执行查询
    cursor = conn.cursor()
    sql = "SELECT path, rewrite FROM ems.ol_ems_interface_config"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(f"查询到 {len(result)} 条数据")
    
    # 打印前5条数据
    for i, row in enumerate(result[:5]):
        print(f"第{i+1}条: path={row[0]}, rewrite={row[1]}")
    
    # 关闭连接
    cursor.close()
    conn.close()
    print("数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")

print("测试完成")
