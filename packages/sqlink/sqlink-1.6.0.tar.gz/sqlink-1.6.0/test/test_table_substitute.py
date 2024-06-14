# -*- coding:utf-8 -*-
from dataclasses import dataclass, asdict

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc, Sql
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


@Dao(entity=Student, fetch_type=Student)
class DaoStudent(DaoFunc):
    @Sql("select * from student where student_id=?;", fetch_type=Student)
    def select_student_by_id(self, student_id):
        pass

    @Sql("select * from __;")
    def select_all_with_substitute(self):
        pass

    @Sql("update __ set name=? where student_id=?;")
    def update_name_by_id_with_substitute(self, name, student_id):
        pass

    @Sql("SELECT * FROM __ WHERE student_id = (SELECT MAX(student_id) FROM __);")
    def select_last_student_with_substitute(self):
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
def test_select_all_with_substitute(db):
    """使用表名替代符"""

    students = insert_data(db)
    results = db.dao_student.select_all_with_substitute()
    for result in results:
        assert asdict(result) == asdict(students[result.student_id])


@use_db(Database)
def test_update_name_with_substitute(db):
    """使用表名替代符更新"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        new_name = '好家伙'
        db.dao_student.update_name_by_id_with_substitute(name=new_name, student_id=select_id)
        db.commit()
        result = db.dao_student.select_student_by_id(select_id)
        assert result[0].name == new_name


@use_db(Database)
def test_multiple_table_substitute(db):
    """复杂sql中同时使用多个表名替代符"""
    students = insert_data(db)
    result = db.dao_student.select_last_student_with_substitute()
    assert result
    assert result[0].student_id == students[-1].student_id


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
