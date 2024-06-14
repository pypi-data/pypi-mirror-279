# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc, Sql
from sqlink.dao import DB_TYPE_SQLITE, DB_TYPE_MYSQL
from sqlink.database import DB
from test.test_env import use_db


@Entity(check_type=True)
@dataclass
class Student:
    name: str = None
    score: int = d.ignore
    address: str = d.ignore
    student_id: int = d.auto_primary_key


@Dao(entity=Student)
class DaoStudent(DaoFunc):
    @Sql("select * from __ where student_id=?;")
    def select_student(self, student_id):
        pass


@DB
class Database:
    dao_student = DaoStudent()


# ====================================================================================================================
@use_db(Database)
def test_ignore(db: Database):
    """数据类的忽略属性在建表时"""
    db.dao_student.create_table()
    db.commit()
    if db.db_type == DB_TYPE_SQLITE:
        db.dao_student.cursor.execute(f"PRAGMA table_info({Student.__name__});")
        # 获取所有列信息
        columns = db.dao_student.cursor.fetchall()
        # 提取并打印所有字段名
        columns = set(column[1] for column in columns)
    elif db.db_type == DB_TYPE_MYSQL:
        sql = """
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION;
                """
        db.dao_student.cursor.execute(sql, ("test_database", Student.__name__))
        columns = db.dao_student.cursor.fetchall()
        columns = set(column[0] for column in columns)

    entity_fields = set(attr_name for attr_name, attr_type in Student.__annotations__.items())
    ignore_fields = {'score', 'address'}
    entity_fields_without_ignore = set(filter(lambda item: item not in ignore_fields, entity_fields))

    assert entity_fields != columns
    assert entity_fields_without_ignore == columns


@use_db(Database)
def test_insert_ignore(db: Database):
    """数据类的忽略属性在插入记录时"""
    student = Student(name='张三', score=100, address='hit')
    db.dao_student.insert(student)
    db.commit()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
