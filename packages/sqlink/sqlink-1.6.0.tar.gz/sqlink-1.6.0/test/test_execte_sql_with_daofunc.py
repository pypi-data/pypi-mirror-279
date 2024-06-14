# -*- coding:utf-8 -*-
from dataclasses import dataclass, asdict

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc
from sqlink.database import DB
from test.test_env import use_db


@Entity(check_type=True)
@dataclass
class Student:
    name: str
    age: int
    phone: int = d.not_null
    weight: float = 50.0, d.not_null
    height: float = d.not_null, d.unique
    address: str = 'hit', d.not_null, d.unique, d.datatype("varchar(200)")
    student_id: int = d.primary_key
    if_aged: bool = False


@Dao(entity=Student, fetch_type=dataclass)
class DaoStudent(DaoFunc):
    def select_one_student(self, student_id: int):
        sql = "select * from student where student_id=?;"
        return self.execute(sql=sql, args=student_id)

    def select_one_student_with_substitute(self, student_id: int):
        sql = "select * from __ where student_id=? limit 1;"
        return self.execute(sql=sql, args=student_id)

    def select_one_student_with_limit(self, student_id: int):
        sql = "select * from student where student_id=? limit 1;"
        return self.execute(sql=sql, args=student_id)

    def select_one_student_with_substitute_and_limit(self, student_id: int):
        sql = "select * from __ where student_id=? limit 1;"
        return self.execute(sql=sql, args=student_id)


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
def test_execute_sql(db: Database):
    """执行sql方法"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student(student_id=select_id)
        assert isinstance(result, list)
        assert list
        assert asdict(result[0]) == asdict(students[select_id])


@use_db(Database)
def test_execute_sql_with_substitute(db: Database):
    """执行sql方法，使用替代符"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student_with_substitute(student_id=select_id)
        assert asdict(result) == asdict(students[select_id])


@use_db(Database)
def test_execute_sql_with_limit(db: Database):
    """执行sql方法，使用limit"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student_with_limit(student_id=select_id)
        assert asdict(result) == asdict(students[select_id])


@use_db(Database)
def test_execute_sql_with_substitute_and_limit(db: Database):
    """执行sql方法，使用替代符和limit"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student_with_substitute_and_limit(student_id=select_id)
        assert asdict(result) == asdict(students[select_id])


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
