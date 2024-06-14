# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc, Sql
from sqlink.database import DB
from test.test_env import use_db


@Entity(check_type=True)
@dataclass
class Student:
    name: str
    age: int
    student_id: int = d.primary_key


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):
    @Sql("select name from __;")
    def select_name_by_id_without_single_field_list(self):
        pass

    @Sql("select name from __ where student_id=? limit 1;")
    def select_name_by_id_without_single_field(self, student_id: int):
        pass

    @Sql("select name from __;", fetch_type=str)
    def select_name_by_id_with_single_field_list(self):
        pass

    @Sql("select name from __ where student_id=? limit 1;", fetch_type=str)
    def select_name_by_id_with_single_field(self, student_id: int):
        pass


@DB
class Database:
    dao_student = DaoStudent()


# ====================================================================================================================
def generate_students(start, end):
    return [
        Student(name=f'李华{i}', age=i, student_id=i)
        for i in range(start, end)
    ]


def insert_data(db: Database, num=100):
    students = generate_students(1, num)
    db.dao_student.insert(students)
    db.commit()
    return students


# ====================================================================================================================
@use_db(Database)
def test_select_one_field(db: Database):
    students = insert_data(db)
    for student in students:
        s1 = db.dao_student.select_name_by_id_without_single_field(student.student_id)
        s2 = db.dao_student.select_name_by_id_with_single_field(student.student_id)
        assert s1.name == student.name
        assert s2 == student.name

        result1 = db.dao_student.select_name_by_id_without_single_field_list()
        result2 = db.dao_student.select_name_by_id_with_single_field_list()
        for item1, item2 in zip(result1, result2):
            assert type(item1.name) == str
            assert type(item2) == str


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
