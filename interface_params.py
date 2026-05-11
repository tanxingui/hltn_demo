#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
描述: 接口参数配置文件，存放接口ID和对应的请求参数
使用方法: 在 INTERFACE_PARAMS 字典中添加或修改接口ID和参数的对应关系
"""

# 接口ID与参数的映射表
# key: ol_ems_interface_config 表的 id
# value: 对应的请求参数（字典格式）
# 注意：
#   - 如果某个接口不需要传参，设置为 NO_PARAMS
#   - 如果某个接口未在此文件中配置，会尝试自动查找但可能失败

NO_PARAMS = "NO_PARAMS_SPECIAL_FLAG"

INTERFACE_PARAMS = {
    "8": {
        "keywords": "",
        "basisType": "2",
        "page": 1,
        "limit": 50
    },

    "12": {
        "time": [
            "2026-03-01",
            "2026-03-31"
        ]
    },

    "9": {
    "basisType": 1,
    "basisId": "88",
    "name": "xg测试一下1",
    "definition": "111111111111111"
    },

    "11":{
    "keywords": "",
    "basisType": "",
    "page": 1,
    "limit": 20
    },

    "21":{
    "tagId": 59,
    "page": 1,
    "limit": 10000
},
    "15":{
    "keywords": "219736516",
    "applyTime": [],
    "userTab": [],
    "userTag": [],
    "vipFlag": "",
    "page": 1,
    "limit": 20,
    "area_keywork": "",
    "time_zone": [],
    "oversea": "foreign"
},

    "1":{
    "page": 1,
    "limit": 20
},
    "4":{
    "groupId": 17,
    "limit": 10000,
    "page": 1
},
    "5":{
    "groupId": 17
},
    "16":{
    "keywords": "219737361",
    "applyTime": [],
    "userTab": [],
    "userTag": [],
    "vipFlag": "",
    "page": 1,
    "limit": 20,
    "area_keywork": "",
    "time_zone": [],
    "oversea": "",
    "attendClass": 0,
    "equationTimeStart": "",
    "equationTimeEnd": "",
    "pageType": 1
},
    
    # 示例：不需要传参的接口
    "14": NO_PARAMS

}


def get_params_by_id(interface_id):
    return INTERFACE_PARAMS.get(str(interface_id))