import inspect
import os


# class MysqlDatabase(MetaDB):
#     def __init__(self):
#         super().__init__()
#         self.update_db_type("mysql")
#
#     def connect(self):
#         connection = pymysql.connect(host='localhost',
#                                      user='root',
#                                      password='123456')
#         self.update_connection(connection)
#         # 删除数据库（如果存在）
#         self.cursor.execute("DROP DATABASE IF EXISTS test_database")
#         self.cursor.execute("CREATE DATABASE IF NOT EXISTS test_database")
#         # 选择使用新创建的数据库
#         self.cursor.execute("USE test_database")


def use_db(database, sql: str = None):
    def decorator(deco_func):
        def wrapper(*args, **kwargs):
            db = database()
            func_path = inspect.getfile(deco_func)
            # 提取文件名（不含扩展名）
            file_name = os.path.splitext(os.path.basename(func_path))[0]
            db_path = os.path.join(os.path.dirname(func_path), f"test_db\\{file_name}.db")
            if not os.path.exists(os.path.dirname(db_path)):
                os.makedirs(os.path.dirname(db_path))

            if os.path.exists(db_path):
                os.remove(db_path)
            db.connect(f"sqlite://{db_path}")
            if sql:
                db.execute(sql)
            db.create_tables()
            deco_func(*args, **kwargs, db=db)
            db.disconnect()
            if os.path.exists(db_path):
                os.remove(db_path)

        return wrapper

    return decorator
