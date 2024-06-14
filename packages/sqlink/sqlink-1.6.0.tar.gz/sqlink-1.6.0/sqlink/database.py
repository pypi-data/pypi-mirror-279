# -*- coding: utf-8 -*-
import copy
import os

from urllib.parse import urlparse, parse_qs


def DB(cls):
    """数据库类的装饰器。

    # 推荐用法
    Example1:
        @DB
        class Database(DBFunc):
            dao1 = DaoStudent()
            dao2 = ...
            dao3 = ...

    # 完整示例
    Example2:
        @Entity
        class Student:  # 定义一个数据类
            name: str
            student_id: int = Define.auto_primary_key

        @Dao(Student)
        class DaoStudent:  # 定义一个数据访问类

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass

        @DB
        class Database:  # 定义一个数据库类，继承元数据库类
            dao1 = DaoStudent()  # 将各个数据访问类实例化为类变量，集中管理，统一对外。
            dao2 = ...
            dao3 = ...


        db = Database()  # 实例化数据库类，并传入数据库路径
        db.connect('sqlite://test.db')  # 连接数据库
        db.create_tables()  # 创建数据表

    Example3:
        @DB
        class Database:
            def __init__(self):
                self.dao1 = DaoStudent()  # 将各个数据访问类实例化为对象属性
                self.dao2 = ...
                self.dao3 = ...
    """

    class Wrapped(cls, DBFunctions):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            params = cls.__dict__ | self.__dict__
            self.dao_list = []
            for attr, value in params.items():
                if hasattr(value, "entity") and hasattr(value, "update_cursor"):
                    new_value = copy.deepcopy(value)
                    setattr(self, attr, new_value)
                    self.dao_list.append(new_value)

    return Wrapped


class DBFunc:
    """由于IDE不能提示装饰器给出的方法，所以可以通过将数据库类继承此接口来获得代码提示。不继承不会造成任何影响，但推荐继承"""

    def connect(self, connect_string: str, *args, **kwargs):
        """通过标准的数据库连接串建立数据库连接，如sqlite数据库的 sqlite://test.db
        和mysql数据库的 mysql://user:password@localhost:3306/test_db """

    def disconnect(self, *args, **kwargs):
        """断开数据库连接"""

    def execute(self, sql: str, args=None, **kwargs):
        """给外部提供的直接执行sql的接口，避免了再调用内部的connection或者cursor"""

    def commit(self, *args, **kwargs):
        """提交事务"""

    def rollback(self, *args, **kwargs):
        """回滚事务"""

    def create_tables(self):
        """当表不存在时，才会创建数据表。因此可以反复调用该方法，而不会产生错误。"""

    def get_create_table_sql(self):
        """返回各个entity的建表sql语句"""


class DBFunctions(DBFunc):
    """元数据库类，提供库级的操作。"""

    def __init__(self, *args, **kwargs):
        self.connection = None
        self.cursor = None
        self.db_type = None
        self.dao_list = None

    def connect(self, connect_string: str, *args, **kwargs):
        result = parse_connection_string(connect_string)
        db_type = result['db_type']
        if db_type == 'sqlite':
            import sqlite3

            self.update_db_type('sqlite')
            self.connection = sqlite3.connect(os.path.normpath(result['database']), *args, **kwargs)
        elif db_type == 'mysql':
            import pymysql

            self.update_db_type('mysql')
            self.connection = pymysql.connect(user=result['username'],
                                              password=result['password'],
                                              host=result['host'],
                                              port=result['port'])
        else:
            raise ValueError(
                "暂不支持的数据库类型"
            )
        self.cursor = self.connection.cursor()
        for dao in self.dao_list:
            dao.update_cursor(cursor=self.cursor)

    def update_db_type(self, db_type: str):
        self.db_type = db_type
        for dao in self.dao_list:
            dao.update_db_type(db_type)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_tables(self):
        for dao in self.dao_list:
            dao.create_table()  # noqa
        self.commit()

    def get_create_table_sql(self) -> list[str]:
        return [dao.get_create_table_sql() for dao in self.dao_list]

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute(self, sql: str, args=None, **kwargs):
        if args:
            self.cursor.execute(sql, args, **kwargs)
        else:
            self.cursor.execute(sql, **kwargs)


def parse_connection_string(string):
    result = {}
    parsed_url = urlparse(string)

    if parsed_url.scheme == 'mysql':
        result['db_type'] = 'mysql'
        result['username'] = parsed_url.username
        result['password'] = parsed_url.password
        result['host'] = parsed_url.hostname
        result['port'] = parsed_url.port
        result['options'] = parse_qs(parsed_url.query)
        result['database'] = os.path.basename(parsed_url.path)
    elif parsed_url.scheme == 'sqlite':
        result['db_type'] = 'sqlite'
    else:
        raise ValueError("数据库连接串格式错误")

    if parsed_url.scheme == 'sqlite':
        if parsed_url.netloc:
            result['database'] = os.path.normpath(parsed_url.netloc + parsed_url.path)
        else:
            result['database'] = os.path.normpath(parsed_url.path)

    return result
