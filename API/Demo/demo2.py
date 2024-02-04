import hashlib
import base64


def md5_parm(msg, md5):
    data = msg + md5
    data_digest = hashlib.md5(data.encode(encoding='utf-8')).hexdigest()
    return base64.b64encode(data_digest.encode(encoding='utf-8')).decode()


if __name__ == '__main__':
    msg_body = '{"traces":[{"opOrgCode":"51800101","opTime":"2017-12-14 19:57:14","opName":"投递结果反馈-妥投","traceNo":"9620140653354","opDesc":"已签收,本人签收 :++,投递员:方焕钦18682231315","operatorNo":"445224198407150938","opCode":"704","opOrgName":"中国邮政集团公司深圳市建设路支局","opOrgProvName":"广东","operatorName":"方焕钦","opOrgCity":"深圳"}]}'
    md5 = "7D9D221E7FAC1FC653FA8B8B90A9C5E5"
    print(md5_parm(msg_body, md5))
