# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc
from sqlink.database import DB
from test.test_env import use_db


@Entity
@dataclass
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
class Database:
    dao_student = DaoStudent()


# ====================================================================================================================
@use_db(Database)
def test_create_tables(db):
    """建库"""
    db.create_tables()


@use_db(Database)
def test_create_with_comment(db):
    """注释功能"""
    db.dao_student.create_table()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
