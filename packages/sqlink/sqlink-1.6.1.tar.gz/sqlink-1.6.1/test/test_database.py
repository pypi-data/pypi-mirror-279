# -*- coding:utf-8 -*-
import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc
from sqlink.database import DB, DBFunc
from test.test_env import use_db


@Entity
class Student_Comment:
    name: str = d.comment('学生姓名')
    contact_info: float = d.comment('联系方式')
    time: str = d.comment('时间')
    abstract: str = d.comment('摘要')
    student_id: int = d.auto_primary_key, d.comment('学生id')


@Dao(Student_Comment)
class DaoStudent(DaoFunc):
    pass


@DB
class Database(DBFunc):
    def __init__(self):
        self.dao_student = DaoStudent()


@DB
class DatabaseStaticDao:
    dao_student = DaoStudent()


@DB
class DatabaseMix:
    dao_student1 = DaoStudent()

    def __init__(self):
        self.dao_student2 = DaoStudent()


# ====================================================================================================================
def test_parse_dao_list():
    db = DatabaseMix()
    assert len(db.dao_list) == 2
    assert db.dao_list[0] is not db.dao_list[1]


def test_multiple_parse_db():
    db1 = Database()
    db2 = Database()
    db3 = DatabaseStaticDao()
    db4 = DatabaseStaticDao()

    assert db1.dao_student is not db2.dao_student
    assert db3.dao_student is not db4.dao_student


@use_db(Database)
def test_create_tables(db):
    """建库"""
    db.create_tables()


@use_db(Database)
def test_create_with_comment(db):
    """注释功能"""
    db.dao_student.create_table()


@use_db(DatabaseStaticDao)
def test_static_dao_create_tables(db):
    """建库"""
    db.create_tables()


@use_db(DatabaseStaticDao)
def test_static_dao_create_with_comment(db):
    """注释功能"""
    db.dao_student.create_table()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
