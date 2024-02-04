import pymysql


class DBConnection:
    def __init__(self, ip='testdb.61info.com', port=3306, user='root', passwd='dbtest', db="i61-hll-manager"):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def getCon(self):
        try:
            conn = pymysql.connect(host=self.ip, port=self.port, user=self.user, passwd=self.passwd,
                                   database=self.db)
            return conn
        except pymysql.Error as e:
            print('数据库连接失败：{}'.format(e))

    def select(self, sql):
        try:
            con = self.getCon()  # 数据库连接对象
            cur = con.cursor()  # 数据库游标对象
            cur.execute(sql)  # 执行数据库命令
            data = cur.fetchall()  # 获取查询数据
            return data
        except pymysql.Error as e:
            print('在查询数据库时发生错误了：{}'.format(e))
        finally:
            cur.close()  # 关闭游标对象
            con.close()  # 关闭连接对象

    def update(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            print('在更新数据库时发生错误了：{}'.format(e))
        finally:
            cur.close()
            con.close()

    def insert(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            print('在插入数据时发生错误了：{}'.format(e))
        finally:
            cur.close()
            con.close()

    def delete(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            print('在删除数据库时发生错误了：{}'.format(e))
        finally:
            cur.close()
            con.close()


if __name__ == '__main__':
    order_id = DBConnection().select(
        "SELECT id from dealer_shop_user_order WHERE order_no = 202203191811458493")
    print(order_id)
