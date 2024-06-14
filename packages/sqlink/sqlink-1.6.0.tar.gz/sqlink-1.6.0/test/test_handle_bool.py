# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc, Sql
from sqlink.database import DB
from test.test_env import use_db


@Entity(check_type=True)
class Student:
    name: str
    age: int
    phone: int = d.not_null
    weight: float = 50.0, d.not_null
    height: float = d.not_null, d.unique
    address: str = 'hit', d.not_null, d.unique, d.datatype("varchar(200)")
    student_id: int = d.primary_key
    if_aged: bool = False


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):

    @Sql("select if_aged from __ limit 1;", fetch_type=bool)
    def select_bool(self):
        pass

    @Sql("select if_aged from __ limit 1;")
    def select_bool_no_return_bool(self):
        pass


@DB
class Database:
    dao_student = DaoStudent()


# ====================================================================================================================
def generate_students(start, end):
    return [
        Student(name=f'李华{i}', age=i, phone=123456789,
                weight=50.0, height=100.0 + i, address=f'hit{i}',
                student_id=i)
        for i in range(start, end)
    ]


def insert_data(db: Database, num=100):
    students = generate_students(0, num)
    db.dao_student.insert(students)
    db.commit()
    return students


# ====================================================================================================================
@use_db(Database)
def test_bool(db: Database):
    insert_data(db, 1000)
    result1 = db.dao_student.select_bool()
    result2 = db.dao_student.select_bool_no_return_bool()
    assert type(result1) == bool
    assert type(result2.if_aged) == int


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
