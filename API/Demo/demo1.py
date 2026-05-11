import json
import requests
from concurrent.futures import ThreadPoolExecutor

# 请求头
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiSUNwa01oNTYxMDVmck92TE1yUmJRamFkdFJjSTBscWUxYytZZCt3SEJuK3FRcnRoWHh0ZTdMZm40cFpUMFpCNW1ZSmxEeGxaWWVZZVhMSkMzcmIzcExxUXlQRjYwYTZxc3NXc0V4cWdiZnVFN3I1eWpIN3lCWkNxM0dvU09EazlBeFZoMDVlYjhHNVFRa0xwcDRiWUp5MW5JY1BiUWRLYmxWUW9CUW9GY00rYnVQWnhNUTVRbmZETnI1UE1kcWlwVEJFTzE3MExnWEY3Y0ZKSnRDTGdwZjR2T0JvczZwanZCS3JRU0dRRElrVzNKQ0ZPMFJkVS9ISlJvWE9wMC9sWWZSbU1UcHBjb1JsMDFiUlFiZXNrR0tBb2FWQXhmdFd1M1dOTmdKSVdpZXAvajQzOHRBMFF5TDNFZkx3UnA1WXJ2emN4RVVxdnZZVTRmckZncEJLRHJ3PT0iLCJleHAiOjE3OTEyNTIyNjl9.N4rusHfwp-uxLWL0qyY59_N5Msj_RMErsDZJ58vYKjI",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://manager-test.61info.cn",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://manager-test.61info.cn/",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

# 请求体（你 curl 里的 --data-raw 完整内容）
payload = {
    "id": 11,
    "language": 2,
    "courseName": "魔力27.1M课件3",
    "courseLabel": 52,
    "courseType": 1,
    "isAdjustCourse": False,
    "bindAdjustCourseId": "",
    "courseMajorMessage": "亲爱的XX家长，课程顾问已经成功为宝贝预约了课程哦\nn课程名称：《魔法条纹》n时间：2015-09-29 8:00~9:00n备注：点击消息查收宝贝的学习手册，了解课程信息、做好课前准备哦~",
    "coverImg": [
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "lALPBE1XYo5Di1zNAYzNAgc_519_396.png",
            "pageSize": 0,
            "resourceId": 217026,
            "url": "https://testimg0.61info.cn/cms/course_img/cover/2020/11/4/1604481820777.png"
        }
    ],
    "newCoverImg": [
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "QQ浏览器截图20200525213742.png",
            "pageSize": 0,
            "resourceId": 217027,
            "url": "https://testimg0.61info.cn/cms/course_img/cover/2020/11/4/1604481836912.png"
        }
    ],
    "courseForm": 1,
    "courseDuration": 70,
    "courseHour": 1,
    "imageLabelIds": [419, 446, 72, 92, 80, 87, 391, 88, 76, 390, 91, 84, 86, 85, 73, 74, 77, 389, 83, 79, 75, 392, 82, 93, 89, 90, 78, 81],
    "coreKnowledgeIds": [6, 3],
    "reviewKnowledgeIds": [7, 4, 8, 9, 10, 11, 12, 13],
    "courseFiles": [
        {
            "courseResourceRelationId": 0,
            "createPage": 1,
            "fileSize": 0,
            "hash": "",
            "name": "1578540152409 (1).pptx",
            "pageSize": 20,
            "resourceId": 223485,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/658e628db172900001cc4956.pptx",
            "uid": 1775701651224,
            "status": "success"
        }
    ],
    "coursewareImgs": [
        {
            "courseResourceRelationId": 3008476,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "1718851231161.jpg",
            "pageSize": 0,
            "resourceId": 226827,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/66d01b4ac98fe40001824865.jpg"
        }
    ],
    "inCourseVideos": [
        {
            "courseVideoRelationId": 31523,
            "id": 142705,
            "name": "4月随报.mp4",
            "url": "https://media6-test.61info.cn/video/91554e71e9e72313aa46728fa8ed3dda/73e609ee-d460-47d8-9fe9-40f2af7b57d7.mp4",
            "uid": 1775701651226,
            "status": "success"
        }
    ],
    "inCourseAudios": [
        {
            "courseVideoRelationId": 30289,
            "id": 142461,
            "name": "测试.mp3",
            "url": "/mnt/web/cmsfile/cms/video/6dd0a420e3cc0fb2df596a3f56eff59f/d72f4e9b-ac56-4b8b-8467-c15b14446000.mp3",
            "uid": 1775701651227,
            "status": "success"
        },
        {
            "courseVideoRelationId": 31293,
            "id": 142650,
            "name": "audio_1690956026281.mp3",
            "url": "https://media6-test.61info.cn/video/49e95b21049d688aee10d682a9347209/853822e2-50a3-438c-b216-6ea583cc47c9.mp3",
            "uid": 1775701651228,
            "status": "success"
        }
    ],
    "classroomExerciseList": [],
    "attachmentInteractionList": [
        {
            "backgroundUrl": [],
            "borderUrl": [],
            "delete": 0,
            "id": 536,
            "imageIsChange": 0,
            "imageRelationList": [
                {"leftOrder": 1, "rightOrder": 1},
                {"leftOrder": 2, "rightOrder": 2}
            ],
            "interactionDuration": -1,
            "leftSideImage": [
                {
                    "name": "左1",
                    "order": 1,
                    "relation": 1,
                    "uid": 1775701650841,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0ef2fb1052200017be28d.png"
                },
                {
                    "name": "左2",
                    "order": 2,
                    "relation": 2,
                    "uid": 1775701650841,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0ef36b1052200017be28e.png"
                }
            ],
            "name": "连线交互5",
            "rightSideImage": [
                {
                    "name": "右1",
                    "order": 1,
                    "relation": 0,
                    "uid": 1775701650841,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0ef332ff99100017b0dec.jpg"
                },
                {
                    "name": "右2",
                    "order": 2,
                    "relation": 0,
                    "uid": 1775701650841,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0ef39b1052200017be28f.jpg"
                }
            ],
            "title": "连线交互5",
            "triggerPage": 2
        },
        {
            "backgroundUrl": [],
            "borderUrl": [],
            "delete": 0,
            "id": 538,
            "imageIsChange": 0,
            "imageRelationList": [
                {"leftOrder": 1, "rightOrder": 1},
                {"leftOrder": 2, "rightOrder": 2}
            ],
            "interactionDuration": -1,
            "leftSideImage": [
                {
                    "name": "左1",
                    "order": 1,
                    "relation": 1,
                    "uid": 1775701650876,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0f651b1052200017be293.jpg"
                },
                {
                    "name": "左2",
                    "order": 2,
                    "relation": 2,
                    "uid": 1775701650876,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0f6542ff99100017b0df3.png"
                }
            ],
            "name": "连线交互2",
            "rightSideImage": [
                {
                    "name": "右1",
                    "order": 1,
                    "relation": 0,
                    "uid": 1775701650876,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0f657b1052200017be294.jpg"
                },
                {
                    "name": "右2",
                    "order": 2,
                    "relation": 0,
                    "uid": 1775701650876,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d0f65a2ff99100017b0df4.png"
                }
            ],
            "title": "连线交互2",
            "triggerPage": 5
        },
        {
            "backgroundUrl": [],
            "borderUrl": [],
            "delete": 0,
            "id": 539,
            "imageIsChange": 0,
            "imageRelationList": [
                {"leftOrder": 1, "rightOrder": 1},
                {"leftOrder": 2, "rightOrder": 2}
            ],
            "interactionDuration": -1,
            "leftSideImage": [
                {
                    "name": "左1",
                    "order": 1,
                    "relation": 1,
                    "uid": 1775701650911,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10ca3f412f900012a20e1.jpg"
                },
                {
                    "name": "左2",
                    "order": 2,
                    "relation": 2,
                    "uid": 1775701650911,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10ca697b7ca000154b264.png"
                }
            ],
            "name": "连线交5",
            "rightSideImage": [
                {
                    "name": "右1",
                    "order": 1,
                    "relation": 0,
                    "uid": 1775701650911,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10ca9f412f900012a20e2.jpg"
                },
                {
                    "name": "右2",
                    "order": 2,
                    "relation": 0,
                    "uid": 1775701650911,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10cadf412f900012a20e3.jpg"
                }
            ],
            "title": "连线交5",
            "triggerPage": 10
        },
        {
            "backgroundUrl": [],
            "borderUrl": [],
            "delete": 0,
            "id": 540,
            "imageIsChange": 0,
            "imageRelationList": [
                {"leftOrder": 1, "rightOrder": 2},
                {"leftOrder": 2, "rightOrder": 1}
            ],
            "interactionDuration": -1,
            "leftSideImage": [
                {
                    "name": "左1",
                    "order": 1,
                    "relation": 2,
                    "uid": 1775701650946,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10e7bf412f900012a20e4.png"
                },
                {
                    "name": "左2",
                    "order": 2,
                    "relation": 1,
                    "uid": 1775701650946,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10e80f412f900012a20e5.png"
                }
            ],
            "name": "test16",
            "rightSideImage": [
                {
                    "name": "右1",
                    "order": 1,
                    "relation": 0,
                    "uid": 1775701650946,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10e8397b7ca000154b265.png"
                },
                {
                    "name": "右2",
                    "order": 2,
                    "relation": 0,
                    "uid": 1775701650946,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10e8597b7ca000154b266.png"
                }
            ],
            "title": "test16",
            "triggerPage": 165
        },
        {
            "backgroundUrl": [],
            "borderUrl": [],
            "delete": 0,
            "id": 541,
            "imageIsChange": 0,
            "imageRelationList": [
                {"leftOrder": 1, "rightOrder": 1},
                {"leftOrder": 2, "rightOrder": 2}
            ],
            "interactionDuration": -1,
            "leftSideImage": [
                {
                    "name": "左1",
                    "order": 1,
                    "relation": 1,
                    "uid": 1775701650982,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10f7297b7ca000154b267.png"
                },
                {
                    "name": "左2",
                    "order": 2,
                    "relation": 2,
                    "uid": 1775701650982,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10f7697b7ca000154b268.png"
                }
            ],
            "name": "test17",
            "rightSideImage": [
                {
                    "name": "右1",
                    "order": 1,
                    "relation": 0,
                    "uid": 1775701650982,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10f74f412f900012a20e6.png"
                },
                {
                    "name": "右2",
                    "order": 2,
                    "relation": 0,
                    "uid": 1775701650982,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/68d10f78f412f900012a20e7.png"
                }
            ],
            "title": "test17",
            "triggerPage": 111
        }
    ],
    "coloringInteractionList": [
        {
            "backgroundUrl": [],
            "borderUrl": [],
            "colors": "FF0000,FF7F00,FFFF00,00FF00,00FFFF,0000FF,8B00FF,00BFFF,2E8B57,8B4513,A9A9A9,F23411",
            "delete": 0,
            "id": 344,
            "imageList": [
                {
                    "colorCode": "F23411",
                    "name": "第1张（最底层）",
                    "order": 1,
                    "uid": 1775701651017,
                    "url": "https://testimg0.61info.cn/rbkd/2020/4/24/1587715277823.png"
                },
                {
                    "colorCode": "F23411",
                    "name": "第2张",
                    "order": 2,
                    "uid": 1775701651017,
                    "url": "https://testimg0.61info.cn/rbkd/2020/4/24/1587715281497.png"
                },
                {
                    "colorCode": "F23411",
                    "name": "第3张",
                    "order": 3,
                    "uid": 1775701651017,
                    "url": "https://testimg0.61info.cn/rbkd/2020/4/24/15877158.png"
                }
            ],
            "interactionDuration": -1,
            "name": "填色交互2",
            "title": "填色交互2",
            "triggerPage": 12
        }
    ],
    "magicKnapsackExerciseList": [],
    "magicKnapsackExerciseListUpdate": [],
    "redPacketRainList": [],
    "stripeMagicExerciseList": [
        {
            "backgroundImgs": [
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 2,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                }
            ],
            "choiceImgs": [
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                },
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                }
            ],
            "dataType": 0,
            "delete": False,
            "id": 79,
            "title": "条纹魔法",
            "triggerPage": 6
        },
        {
            "backgroundImgs": [
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 2,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                },
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 2,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                }
            ],
            "choiceImgs": [
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                },
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                },
                {
                    "choiceSort": "",
                    "name": "",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/9/21/1600669974732.png"
                },
                {
                    "choiceSort": "4",
                    "name": "选项 4",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/10/10/1602310970887.png"
                },
                {
                    "choiceSort": "5",
                    "name": "选项 5",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/10/10/1602310974461.png"
                },
                {
                    "choiceSort": "6",
                    "name": "选项 6",
                    "type": 1,
                    "url": "https://testimg0.61info.cn/rbkd/2020/10/10/1602310980446.png"
                }
            ],
            "dataType": 0,
            "delete": False,
            "id": 80,
            "title": "条纹魔法2233",
            "triggerPage": 8
        }
    ],
    "newCoursePreviewVideos": [
        {
            "courseVideoRelationId": 31526,
            "id": 142706,
            "name": "4月随报.mp4",
            "url": "https://media6-test.61info.cn/video/91554e71e9e72313aa46728fa8ed3dda/2afe0783-50a2-420f-9996-bea273bffc38.mp4",
            "uid": 1775701651261,
            "status": "success"
        }
    ],
    "beforeCourseVideos": [],
    "courseFocusVideos": [],
    "drawingShowVideoRelationGathers": [
        {
            "courseVideoRelationFileDtos": [
                {
                    "courseVideoRelationFileId": 1259,
                    "fileHash": "",
                    "fileSize": 0,
                    "name": "LP业务单工作台作业流程.png",
                    "orderNum": 1,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/6434f913ab2e930001182b2c.png",
                    "uid": 1775701651262,
                    "status": "success"
                }
            ],
            "courseVideoRelationId": 31715,
            "videoId": 142502,
            "videoName": "视频.mp4",
            "videoUrl": "https://media6-test.61info.cn/video/90769cbb99c4c49ad4c78f8a838f564d/b055ba1a-9ccd-4e7f-b527-9ca7ed52d52d.mp4",
            "uid": 1775701651263,
            "status": "success"
        },
        {
            "courseVideoRelationFileDtos": [
                {
                    "courseVideoRelationFileId": 1260,
                    "fileHash": "",
                    "fileSize": 0,
                    "name": "潇潇（485）_美术小班红包邀请卡_CMS_20230406111059.png",
                    "orderNum": 1,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/643521fb6578d70001e7da7f.png",
                    "uid": 1775701651263,
                    "status": "success"
                }
            ],
            "courseVideoRelationId": 31716,
            "videoId": 142504,
            "videoName": "5.mp4",
            "videoUrl": "https://media6-test.61info.cn/video/3c746f1caac31f46699356f4e79aa123/1e853142-8beb-4521-8770-34f32b1b4660.mp4",
            "uid": 1775701651264,
            "status": "success"
        }
    ],
    "summarizeAfterClassImgList": [],
    "needCommitHomework": 1,
    "hasCreativeWork": 0,
    "creativeWorkMessage": "",
    "hasParentWork": 0,
    "parentWorkMessage": "",
    "courseDemoImgs": [
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "lADPBE1XdLPAfNnNAbzNAbs_443_444.jpg",
            "pageSize": 0,
            "resourceId": 217152,
            "url": "https://testimg0.61info.cn/cms/course_img/demo/2020/11/16/1605510139198.jpg",
            "uid": 1775701651265,
            "status": "success"
        }
    ],
    "paintingResources": [
        {
            "name": "223122-1536762682439c.jpg",
            "paintingResourceId": 0,
            "relationId": 1261,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/63e351104798a90001533081.jpg",
            "uid": 1775701651267,
            "status": "success"
        },
        {
            "name": "222731-1583504851c1b2.jpg",
            "paintingResourceId": 0,
            "relationId": 1262,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/63e351104798a90001533082.jpg",
            "uid": 1775701651268,
            "status": "success"
        },
        {
            "name": "7a6f68d6-dc1c-4385-a5e3-3252ea267e29.jpg",
            "paintingResourceId": 0,
            "relationId": 1263,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/63e351114798a90001533083.jpg",
            "uid": 1775701651269,
            "status": "success"
        },
        {
            "name": "16pic_7513082_b.png",
            "paintingResourceId": 0,
            "relationId": 1303,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/6434f2986343301408ab466b.png",
            "uid": 1775701651270,
            "status": "success"
        }
    ],
    "materialImgList": [
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "chwg0ryoj2c.jpg",
            "pageSize": 0,
            "resourceId": 227350,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/66f3d55de3f4b200011e568a.jpg",
            "uid": 1775701651268,
            "status": "success"
        },
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "1677573205966.jpg",
            "pageSize": 0,
            "resourceId": 227640,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/672d8b37185d8f0001283062.jpg",
            "uid": 1775701651269,
            "status": "success"
        }
    ],
    "coursePreviewList": [
        {
            "imgUrls": [
                {
                    "courseResourceRelationId": 0,
                    "createPage": 0,
                    "fileSize": 0,
                    "hash": "",
                    "name": "1587622005171.png",
                    "pageSize": 0,
                    "resourceId": 215418,
                    "url": "https://testimg0.61info.cn/cms/course_img/other/2020/8/13/1597324999714.png",
                    "uid": 1775701651260,
                    "status": "success"
                },
                {
                    "courseResourceRelationId": 0,
                    "createPage": 0,
                    "fileSize": 0,
                    "hash": "",
                    "name": "ai.jpg",
                    "pageSize": 0,
                    "resourceId": 224523,
                    "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/663c408b2d0d9b0001f13945.jpg",
                    "uid": 1775701651261,
                    "status": "success"
                }
            ],
            "previewText": "122222222"
        }
    ],
    "homeworkTeacherType": 3,
    "bigCourseCommentAccount": "",
    "commentGuide": "333333333",
    "wordFile": [
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "小艺术家《植物大观园》备课文档.docx",
            "pageSize": 0,
            "resourceId": 223805,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/65d45588f13aaa0001b075c5.docx",
            "uid": 1775701651270,
            "status": "success"
        }
    ],
    "guideCourseVideos": [],
    "examinationVOList": [],
    "defaultWorkReview": "原来灯光也会“变魔术”呢，你完成的很好哦！把彩色胶片叠上去，整个房间的氛围感“唰”的一下就出来了呢~今天我们体验了色彩和光线对画面的变化和影响，还复习了物体的立体刻画，以后我们也可以用这样的方法营造画面氛围感哦！11",
    "enableSelfStudy": False,
    "selfStudySlides": [
        {
            "courseResourceRelationId": 0,
            "createPage": 0,
            "fileSize": 0,
            "hash": "",
            "name": "《五颜六色的“面”》自习室.pptx",
            "pageSize": 0,
            "resourceId": 223482,
            "url": "https://hualala-common.oss-cn-shenzhen.aliyuncs.com/test/cms/658e6003f275a90001b3f105.pptx",
            "uid": 1775701651271,
            "status": "success"
        }
    ],
    "selfStudyVideo": [
        {
            "courseVideoRelationId": 30584,
            "id": 142609,
            "name": "《五颜六色的“面”》自习室课程视频.mp4",
            "url": "https://media6-test.61info.cn/video/25058097cbe903c67750d16602dfe55b/ca2aa88b-b3f5-4b4c-9c60-956e40874e7d.mp4",
            "uid": 1775701651271,
            "status": "success"
        }
    ],
    "isChangeProcessResource": False,
    "courseVersion": 11
}

url = "https://gw-mg-test.61info.cn/manager-api/o/course/info/update.json"


def call_once():
    """单次调用接口"""
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        return {
            "code": resp.status_code,
            "data": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
        }
    except Exception as e:
        return {"error": str(e)}


def call_concurrent(count=2):
    """并发调用count次"""
    with ThreadPoolExecutor(max_workers=count) as executor:
        futures = [executor.submit(call_once) for _ in range(count)]
        results = [f.result() for f in futures]
    return results


if __name__ == "__main__":
    # 并发调用2次
    result = call_concurrent(2)
    # 格式化输出JSON
    print(json.dumps(result, indent=4, ensure_ascii=False))