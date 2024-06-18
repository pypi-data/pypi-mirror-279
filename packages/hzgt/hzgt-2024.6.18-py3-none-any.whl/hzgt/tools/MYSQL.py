import os

from ..strop import restrop
from ..CONST import INSTALLCMD
from ..sc import SCError

try:
    import pymysql
except Exception as err:
    print(err)
    os.system(INSTALLCMD("pymysql==1.1.0"))
    import pymysql


class Mysqldbop(object):
    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    def __init__(self, mysql_host: str, mysql_port: int, mysql_user: str, mysql_passwd: str,
                 Bool_Show=True, Bool_exit=False):
        """
        初始化并连接数据库

        :param mysql_host: MYSQL服务器IP地址
        :param mysql_port: MYSQL端口
        :param mysql_user: 账号
        :param mysql_passwd: 密码
        :param Bool_Show: 是否显示提示信息
        """
        config = {"host" : mysql_host,
                  "port" : int(mysql_port),
                  "user" : mysql_user,
                  "passwd" : mysql_passwd,
                  'charset': 'utf8'}

        self.con = None
        self.cur = None
        self.selecteddb = None  # 已选择的数据库
        self.selectedtable = None  # 已选择的数据库表格
        self.connection = False
        self.Bool_Show = Bool_Show

        try:
            self.con = pymysql.connect(**config)
            self.con.autocommit(0)
            self.cur = self.con.cursor()
            if self.Bool_Show:
                print(f"用户{restrop(config['user'], f=2)}已连接数据库. . .")
            self.Bool_connection = True
        except Exception as err:
            self.connection = False
            if Bool_exit:
                print(restrop(f"数据库连接失败. Error: {err}"))
                exit(-1)
            else:
                raise SCError(f'数据库连接失败. Error: {err}')

    # 关闭数据库连接
    def __del__(self):
        """
        删除对象时调用__del__()关闭连接
        """
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return exc_type, exc_val, exc_tb

    # 关闭数据库连接
    def close(self):
        """
        断开连接
        :return: None
        """
        if self.con:
            self.cur.close()
            self.con.close()
            self.con = None
            self.cur = None
            if self.Bool_Show:
                print(restrop("数据库连接已关闭. . ."))
            del self

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    # 查看当前用户
    def look_current_user(self):
        """
        查看当前用户
        :return: resu 当前用户
        """
        sql = "select user();"
        resu = self.executeSql(sql)
        # print("当前用户: ", resu)
        return resu

    # 获取数据库版本号
    def get_version(self):
        """
        查看数据库版本
        :return: vers 数据库版本
        """
        vers = self.cur.execute("SELECT VERSION()")
        # print("数据库版本号: ", vers)
        return vers

    # 获取上个查询的结果
    def get_last_Data(self):
        """
        查看上一个查询的结果
        :return: data 上一次查询的结果
        """
        # 取得上个查询的结果，是单个结果
        data = self.cur.fetchone()
        # print("上个查询结果: ", data)
        return data

    # 查看所有数据库
    def get_all_db(self):
        """
        查看所有数据库
        :return: vers 所有数据库
        """
        vers = self.executeSql("show databases;")
        # print("所有数据库: ", vers)
        return vers

    # 查看所有非系统数据库
    def get_all_nonsys_db(self):
        """
        获取所有数据库名
        :return: list
        """
        # 排除自带的数据库
        exclude_list = ["sys", "information_schema", "mysql", "performance_schema"]
        res = self.get_all_db()
        if not res:  # 判断结果非空
            return False

        db_list = []  # 数据库列表
        for i in res:
            db_name = i[0]
            # 判断不在排除列表时
            if db_name not in exclude_list:
                db_list.append(db_name)
        if not db_list:
            return False
        else:
            # print(f"所有非系统数据库: {db_list}")
            return db_list

    # 查看已选择的数据库的所有表
    def get_tables(self):
        """
        查看已选择的数据库的所有表
        :return: tables 所有表格
        """
        tables = self.executeSql("show tables;")
        # print(f"数据库[{restrop(self.selecteddb, f=4)}] 的所有表: ", tables)
        return tables

    # 查看表索引
    def get_Table_indexes(self, tablename: str = ''):
        """
        查看表索引
        :param tablename: 表名
        :return: resu 表的索引
        """
        if not tablename:
            tablename = self.selectedtable
        sql = f"desc {tablename}"
        resu = self.executeSql(sql)
        # print(f"数据库[{restrop(self.selecteddb, f=4)}] 的 表[{restrop(tablename, f=4)}] 的索引: ", resu)
        return resu

    def diy(self, sql: str):
        """
        自定义指令
        :param sql: str
        :return: None
        """
        resu = self.executeSql(sql)
        # print(restrop(f"DIY: {sql} ==>>", f=5), resu)
        return resu

    # 选择数据库
    def selectDataBase(self, DB_NAME: str):
        """
        选择数据库
        :param DB_NAME: str 待选择的数据库的表格
        :return: None
        """
        self.con.select_db(DB_NAME)
        self.selecteddb = DB_NAME
        # print(f"已选择 数据库[{restrop(DB_NAME, f=4)}]")
        return None

    # 选择数据库表
    def selectTable(self, Table_name: str):
        self.selectedtable = Table_name

    # 创建数据库
    def createDataBase(self, DB_NAME: str):
        sql = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci" % DB_NAME
        # 创建数据库
        self.cur.execute(sql)
        # print(f'已创建 数据库[{restrop(DB_NAME, f=4)}]')
        self.selectDataBase(DB_NAME)

    # 删除数据库
    def dropDataBase(self, DB_NAME: str):
        sql = f"DROP DATABASE IF EXISTS {DB_NAME};"
        # 删除数据库
        self.cur.execute(sql)
        # print(f'已删除 数据库[{restrop(DB_NAME, f=4)}]')
        self.selecteddb = None

    # 创建数据库表
    def creatTable(self, tablename: str, attrdict: dict, constraint: str = "PRIMARY KEY(`id`)"):
        """创建数据库表

            args:
                tablename : 表名字\n
                attrdict : 属性键值对,{'book_name':'varchar(200) NOT NULL'...}\n
                constraint : 主外键约束,PRIMARY KEY(`id`)\n
        """
        # 　判断表是否存在
        # if self.isExistTable(tablename):
        #     print("%s is exit" % tablename)
        #     return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr, value in attrdict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s(' % tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        # print(restrop('creat table: ', f=2) + sql)
        self.executeCommit(sql)
        # print(f"已在 数据库[{restrop(self.selecteddb, f=4)}] 创建 表格[{restrop(tablename, f=4)}]")

    def executeSql(self, sql: str = ''):
        """
            执行sql语句，针对读操作返回结果集

            args:
                sql : sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except pymysql.Error as e:
            error = '执行sql语句失败(%s): %s' % (e.args[0], e.args[1])
            # print(error)
            raise SCError(error)

    def executeCommit(self, sql: str = ''):
        """
        执行数据库sql语句，针对更新,删除,事务等操作失败时回滚
        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except pymysql.Error as err:
            self.con.rollback()
            error = '执行数据库sql语句失败(%s): %s' % (err.args[0], err.args[1])
            # print("error:", restrop(error))
            raise SCError(error)

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    # 插入数据
    def insert(self, tablename: str = '', params: dict = None):
        """
        往表里插入数据，单条数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                key : 属性键\n
                value : 属性值\n
        """
        if not tablename:
            tablename = self.selectedtable
        key = []
        value = []
        for k, v in params.items():
            key.append('`' + k + '`')
            value.append("'" + v + "'")
            # print(value)
        sql = 'insert into %s' % tablename
        # sql = sql + attrs_sql + values_sql
        sql = sql + ' (' + ','.join(key) + ')' + ' values ' + "(" + ",".join(value) + ")"
        # print(restrop('insert: ', f=2) + sql)
        self.executeCommit(sql)
        # print(f"对 表[{restrop(tablename, f=4)}] 的 表格[{restrop(tablename, f=4)}] 插入数据成功")

    def select(self, tablename: str = '', cond_dict: dict = None, order='', fields: list = '*'):
        """
        查询数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                cond_dict : 查询条件\n
                order : 排序条件\n
            example:
                mydb.select(table)\n
                mydb.select(table, cond_dict={"name": "admin"})\n
                mydb.select(table, fields=["name"])\n
                mydb.select(table, fields=["name", "age"])\n
                mydb.select(table, fields=["age", "name"])\n
        """
        if not tablename:
            tablename = self.selectedtable
        if cond_dict is None:
            cond_dict = {}
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                consql = consql + '`' + k + '`' + '=' + '"' + v + '"' + ' and'
        consql = consql + ' 1=1 '
        sql = ""
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                error = "fields参数数据输入有误"
                raise SCError(error)
        sql = sql + consql + order
        # print(restrop('select: ', f=2) + sql)
        resu = self.executeSql(sql)
        # print(f"对 表[{restrop(tablename, f=4)}] 的 列[{restrop(fields, f=4)}] 查询结果: ", resu)
        return resu

    def delete(self, tablename: str = '', cond_dict: dict = None):
        """
        删除数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                cond_dict : 删除条件字典\n
            example:
                params = {"name" : "caixinglong", "age" : "38"}\n
                mydb.delete(table, params)\n
        """
        if not tablename:
            tablename = self.selectedtable
        consql = ' '
        if cond_dict != None:
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where %s" % (tablename, consql)
        # print(restrop("delete: ") + sql)
        return self.executeCommit(sql)

    def update(self, tablename: str = '', attrs_dict: dict = None, cond_dict: dict = None):
        """
        更新数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                attrs_dict : 更新属性键值对字典\n
                cond_dict : 更新条件字典\n
            example:
                params = {"name" : "caixinglong", "age" : "38"}\n
                cond_dict = {"name" : "liuqiao", "age" : "18"}\n
                mydb.update(table, params, cond_dict)\n
        """
        if not tablename:
            tablename = self.selectedtable
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" + "\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        # print(restrop("attrs_sql: ", f=6), attrs_sql)
        if cond_dict != '':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename + "`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        # print(restrop("update: ", f=4) + sql)
        return self.executeCommit(sql)

    def dropTable(self, tablename: str = ''):
        """
        删除数据库表
        默认操作已选择的表格
            args:
                tablename : 表名字
        """
        if not tablename:
            tablename = self.selectedtable
        sql = "DROP TABLE  %s" % tablename
        # print(restrop("drop: ") + sql)
        self.executeCommit(sql)
        # print(f"已删除 数据库[{restrop(self.selecteddb, f=4)}] 的 表格[{restrop(tablename, f=4)}]")

    def deleteTable(self, tablename: str = ''):
        """
        清除数据库表
        默认操作已选择的表格
            args:
                tablename : 表名字
        """
        if not tablename:
            tablename = self.selectedtable
        sql = "DELETE FROM %s" % tablename
        # print(restrop("delete table: ") + sql)
        self.executeCommit(sql)
        # print(f"已清除 数据库[{restrop(self.selecteddb, f=4)}] 的 表格[{restrop(tablename, f=4)}] 的所有内容")

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    # 修改密码
    def change_passwd(self, hostname: str, newpasswd: str, hostip: str = "%"):
        """
        修改密码
        :param hostname: 用户名 '{hostname}'@'{hostip}'
        :param newpasswd: 新密码 IDENTIFIED BY '{newpasswd}'
        :param hostip: ip地址 '{hostname}'@'{hostip}'
        :return:
        """
        sql = f"ALTER USER '{hostname}'@'{hostip}' IDENTIFIED BY '{newpasswd}';"
        # print(restrop("change passwd: ") + sql)
        self.executeCommit(sql)
        # print(restrop(f"密码已修改, 请记住新密码, 并重新登陆. . ."))
        self.close()
