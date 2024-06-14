# -*- coding:utf-8 -*-
from dataclasses import asdict, dataclass

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


@Dao(entity=Student, fetch_type=dataclass)
class DaoStudent(DaoFunc):

    @Sql("select * from student;")
    def select_all(self):
        pass

    @Sql("select * from student where student_id=?;", fetch_type=Student)
    def select_student_by_id(self, student_id):
        pass

    @Sql("update student set name=? where student_id=?;")
    def update_name_by_id(self, name, student_id):
        pass

    @Sql("delete from student where student_id=?;")
    def delete_student_by_id(self, student_id):
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
def test_dao_create_table(db):
    """创建表"""
    db.dao_student.create_table()
    db.commit()


@use_db(Database)
def test_insert(db):
    """插入数据"""
    students = generate_students(0, 100)
    for student in students:
        record_id = db.dao_student.insert(entity=student)
        db.commit()

        result = db.dao_student.select_student_by_id(record_id)
        result = result[0]
        assert asdict(result) == asdict(students[result.student_id])


@use_db(Database)
def test_select_all(db):
    """查询全部"""
    students = insert_data(db)
    results = db.dao_student.select_all()
    for result in results:
        assert asdict(result) == asdict(students[result.student_id])


@use_db(Database)
def test_select_student_by_id(db):
    """具体查询"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_student_by_id(student_id=select_id)
        assert asdict(result[0]) == asdict(students[select_id])


@use_db(Database)
def test_update_name(db):
    """更新"""
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        new_name = '好家伙'
        db.dao_student.update_name_by_id(name=new_name, student_id=select_id)
        db.commit()
        result = db.dao_student.select_student_by_id(select_id)
        assert result[0].name == new_name


@use_db(Database)
def test_insert_many(db):
    """批量插入"""
    start = 101
    end = 200
    students2 = generate_students(start=start, end=end)
    db.dao_student.insert(entity=students2)
    db.commit()

    for i in range(start, end):
        result = db.dao_student.select_student_by_id(i)
        result = result[0]
        assert asdict(result) == asdict(students2[i - start])


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
