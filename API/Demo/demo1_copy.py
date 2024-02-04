# debugtalk.py
# 可以使用GLOBAL_VAR['']引用环境变量
import json
import MySQLdb
import datetime
from dateutil.relativedelta import relativedelta



class DBOperate:
    def __init__(self):
        self.host = 'testdb.61info.com'
        self.port = 3306
        self.user = 'root'
        self.passwd = 'dbtest'

    def sql_select(self, sql_expression):
        self._connect()
        try:
            self.cur.execute(sql_expression)
            result = self.cur.fetchall()
            user = [user[0] for user in result]
            return user[0]
        except MySQLdb.Error as e:
            print("Mysql Error select from account")
            result = []
        finally:
            self._disconnect()


    def _connect(self):
        try_count = 0
        while try_count < 2:
            try_count = try_count + 1
            try:
                self.conn = MySQLdb.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.passwd,
                    charset='utf8'
                )
                # self.conn = sqlite3.connect('E:/workspace/11/db.sqlite3')
                self.cur = self.conn.cursor()
                break
            except MySQLdb.Error as e:
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def _disconnect(self):
        # 关闭数据库连接
        try:
            self.cur.close()
            self.conn.commit()
            self.conn.close()
        #             time.sleep(1)
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

print(DBOperate().sql_select("SELECT user_status FROM `i61-hll-manager`.`user_daily_info` WHERE `user_id` = '22171';"))
