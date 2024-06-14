# -*- coding:utf-8 -*-
import time
from collections import namedtuple
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


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):
    @Sql("select * from student;")
    def select_all(self):
        pass

    @Sql("select name, age,phone,weight, height,address,student_id,if_aged from student;", fetch_type=Student)
    def select_all_full(self):
        pass

    @Sql("select name, age,phone,weight, height,address,student_id from student;", fetch_type=Student)
    def select_all_part(self):
        pass

    @Sql("select age,name, student_id,weight, height,if_aged,address,phone from student;", fetch_type=Student)
    def select_all_full_no_order(self):
        pass

    @Sql("select age,name, student_id,weight, height,address,phone from student;", fetch_type=Student)
    def select_all_part_and_no_order(self):
        pass

    @Sql("select * from student;", fetch_type=namedtuple)
    def select_all_namedtuple(self):
        pass

    @Sql("select * from student where student_id=?;", fetch_type=Student)
    def select_student_by_id(self, student_id):
        pass

    @Sql("select * from student where student_id=? limit 1;", fetch_type=Student)
    def select_student_by_id_limit1(self, student_id):
        pass


@Dao(entity=Student, fetch_type=dict)
class DaoStudentDict(DaoFunc):
    @Sql("select * from student;")
    def select_all(self):
        pass

    @Sql("select * from student where student_id=? limit 1;")
    def select_student_by_id(self, student_id):
        pass

    @Sql("select * from student where student_id=?;")
    def select_student_by_id2(self, student_id):
        pass


@Dao(entity=Student, fetch_type=tuple)
class DaoStudentTuple(DaoFunc):
    @Sql("select * from student;")
    def select_all(self):
        pass

    @Sql("select * from student where student_id=? limit 1;")
    def select_student_by_id(self, student_id):
        pass

    @Sql("select * from student where student_id=?;")
    def select_student_by_id2(self, student_id):
        pass


@DB
class Database:
    dao_student = DaoStudent()
    dao_student_dict = DaoStudentDict()
    dao_student_tuple = DaoStudentTuple()


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
def test_row_factory(db: Database):
    start = time.time()
    students = generate_students(0, 100000)
    print(f'\n生成耗时：{time.time() - start}')

    start = time.time()
    db.dao_student.insert(students)
    db.commit()
    end = time.time() - start
    print(f'插入耗时：{end}')

    # 默认数据类
    start = time.time()
    results2 = db.dao_student.select_all()
    end = time.time() - start
    print(f'entity_auto耗费时间：{end}, 查询结果数量；{len(results2)}')

    start = time.time()
    results3 = db.dao_student.select_all_full()
    end = time.time() - start
    print(f'entity_full_fast耗费时间：{end}, 查询结果数量；{len(results3)}')

    start = time.time()
    results4 = db.dao_student.select_all_part()
    end = time.time() - start
    print(f'entity_part耗费时间：{end}, 查询结果数量；{len(results4)}')

    start = time.time()
    results5 = db.dao_student.select_all_full_no_order()
    end = time.time() - start
    print(f'entity_full_not_order耗费时间：{end}, 查询结果数量；{len(results5)}')

    start = time.time()
    result6 = db.dao_student.select_all_part_and_no_order()
    end = time.time() - start
    print(f'entity_part_and_no_order耗费时间：{end}, 查询结果数量；{len(results4)}')
    assert results4 == result6
    assert results2 == results3 == results5

    start = time.time()
    results_dataclass = db.dao_student.select_all()
    end = time.time() - start
    print(f'dataclass耗费时间：{end}, 查询结果数量；{len(results_dataclass)}')

    start = time.time()
    results_dict = db.dao_student_dict.select_all()
    end = time.time() - start
    print(f'dict耗费时间：{end}, 查询结果数量；{len(results_dict)}')

    start = time.time()
    results_tuple = db.dao_student_tuple.select_all()
    end = time.time() - start
    print(f'tuple耗费时间：{end}, 查询结果数量；{len(results_tuple)}')

    start = time.time()
    results_namedtuple = db.dao_student.select_all_namedtuple()
    end = time.time() - start
    print(f'namedtuple耗费时间：{end}, 查询结果数量；{len(results_namedtuple)}')

    for item_dataclass, item_dict, item_tuple, item_namedtuple in zip(results_dataclass,
                                                                      results_dict,
                                                                      results_tuple,
                                                                      results_namedtuple):
        assert item_dict == item_namedtuple._asdict()
        assert item_tuple == item_namedtuple
        assert item_namedtuple._asdict() == asdict(item_dataclass)


@use_db(Database)
def test_dao_return_type_default_list(db: Database):
    students = insert_data(db)
    for student in students:
        result = db.dao_student.select_student_by_id(student.student_id)
        assert result
        assert isinstance(result[0], Student)
        assert result[0] == student


@use_db(Database)
def test_dao_return_type_default(db: Database):
    students = insert_data(db)
    for student in students:
        result = db.dao_student.select_student_by_id_limit1(student.student_id)
        assert isinstance(result, Student)
        assert result == student


@use_db(Database)
def test_dao_return_type_dict_list(db: Database):
    students = insert_data(db)
    for student in students:
        result = db.dao_student_dict.select_student_by_id2(student.student_id)
        assert result
        assert isinstance(result[0], dict)
        assert result[0] == asdict(student)


@use_db(Database)
def test_dao_return_type_dict(db: Database):
    students = insert_data(db)
    for student in students:
        result = db.dao_student_dict.select_student_by_id(student.student_id)
        assert isinstance(result, dict)
        assert result == asdict(student)


@use_db(Database)
def test_dao_return_type_tuple_list(db: Database):
    students = insert_data(db)
    for student in students:
        result = db.dao_student_tuple.select_student_by_id2(student.student_id)
        assert result
        assert isinstance(result[0], tuple)
        assert result[0] == tuple(asdict(student).values())


@use_db(Database)
def test_dao_return_type_tuple(db: Database):
    students = insert_data(db)
    for student in students:
        result = db.dao_student_tuple.select_student_by_id(student.student_id)
        assert isinstance(result, tuple)
        assert result == tuple(asdict(student).values())


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
