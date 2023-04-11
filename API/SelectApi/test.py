import pymysql
import time
conn = pymysql.connect(
    host="172.16.253.113",
    port=3306,
    user='root',
    password='dbtest',
    database='pjx',
    charset='utf8'
)
cursor = conn.cursor()
a = 10
b = 1
startTime = time.time()
with open("test.txt", "w+") as f:  # 这里加一个是为了不用循环后手动去清空数据，w+代表覆盖写入
    f.write('user_id\n')
while b <= a:
    sql = "SELECT user_id FROM `user` where sex = 1 ORDER BY RAND() LIMIT 102"
    cursor.execute(sql)
    data = cursor.fetchall()
    # cursor.close()  #关闭链接
    user_Idlist = []
    for user in data:
        user2 = user[0]
        user_Idlist.append(user2)
    # print(user_Idlist)
    with open("test.txt", "a") as f:
        f.write('{}'';\n'.format(user_Idlist))  # 需要加个分号，因为要匹配jmeter的csv分割符;换行
    b += 1
endTime = time.time()
print('耗时:', '%.2f' % (endTime - startTime), "秒", sep='')
