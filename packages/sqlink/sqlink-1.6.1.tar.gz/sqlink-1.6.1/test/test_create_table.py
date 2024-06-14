# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc
from sqlink.database import DB
from test.test_env import use_db


@Entity
@dataclass
class Student:
    name: str
    age: int
    phone: int = d.not_null
    weight: float = 50.0, d.not_null
    height: float = d.not_null, d.unique
    address: str = 'hit', d.not_null, d.unique, d.datatype("varchar(200)")
    student_id: int = d.auto_primary_key
    if_aged: bool = False


@Dao(Student)
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
def test_create(db):
    db.dao_student.create_table()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
