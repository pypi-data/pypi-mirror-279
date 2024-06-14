# -*- coding:utf-8 -*-
import sqlite3
from dataclasses import dataclass
from typing import Optional

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc, Insert
from sqlink.dao import Conflict, Sql, DB_TYPE_SQLITE, DB_TYPE_MYSQL
from sqlink.database import DB
from test.test_env import use_db


@Entity(check_type=True)
@dataclass
class Student:
    name: str = d.unique, d.datatype("varchar(200)")
    age: int = None
    id: int = d.auto_primary_key


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):

    @Insert(conflict=Conflict.error)
    def insert_error(self):
        pass

    @Insert(conflict=Conflict.ignore)
    def insert_ignore(self):
        pass

    @Insert(conflict=Conflict.replace)
    def insert_replace(self):
        pass

    @Sql("select * from __ where name=? limit 1;")
    def get_student_by_name(self, name) -> Optional[Student]:
        pass


@DB
class Database:
    dao_student = DaoStudent()


students = [Student(name='张三', age=10),
            Student(name='张三', age=11),
            Student(name='李四', age=12)]


# ====================================================================================================================

@use_db(Database)
def test_insert_default(db: Database):
    if db.db_type == DB_TYPE_SQLITE:
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert(student)
        assert "UNIQUE constraint failed" in str(exc_info.value)
    elif db.db_type == DB_TYPE_MYSQL:
        import pymysql

        with pytest.raises(pymysql.err.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert(student)
        assert "Duplicate entry" in str(exc_info.value)
        assert "for key 'student.name'" in str(exc_info.value)
    db.rollback()


@use_db(Database)
def test_insert_error(db: Database):
    if db.db_type == DB_TYPE_SQLITE:
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert_error(student)
        assert "UNIQUE constraint failed" in str(exc_info.value)
    elif db.db_type == DB_TYPE_MYSQL:
        import pymysql

        with pytest.raises(pymysql.err.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert_error(student)
        assert "Duplicate entry" in str(exc_info.value)
        assert "for key 'student.name'" in str(exc_info.value)
    db.rollback()


@use_db(Database)
def test_insert_ignore(db: Database):
    for student in students:
        db.dao_student.insert_ignore(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == select_student.age


@use_db(Database)
def test_insert_replace(db: Database):
    for student in students:
        db.dao_student.insert_replace(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == students[1].age


@use_db(Database)
def test_insert_replace_on_primary_key(db: Database):
    students = [Student(name='张三', age=10, id=1),
                Student(name='张三', age=11, id=1)]
    for student in students:
        db.dao_student.insert_replace(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == students[1].age


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
