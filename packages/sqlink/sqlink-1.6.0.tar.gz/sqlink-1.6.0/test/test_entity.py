# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink.entity import _parse_attr_value, Entity, Define as d


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


def test_simple_create():
    @Entity  # 表明这是数据（表）类
    @dataclass
    class Student:  # 类名即表名，不区分大小写
        score: float
        name: str = '好家伙', d.not_null  # 同时设置默认值和约束，以逗号分开即可
        student_id: int = d.auto_primary_key  # Define类提供多种字段约束

    student = Student(name="李华", score=95.6)
    print(student)


def test_without_check_type():
    @Entity
    @dataclass
    class StudentNoCheck:
        name: str
        age: int = 10
        phone: int = d.not_null
        weight: float = 50.0, d.not_null
        height: float = d.not_null, d.unique
        address: str = 'hit', d.not_null, d.unique
        student_id: int = d.auto_primary_key

    student = StudentNoCheck(name=f'李华', age=1, phone=123456789,
                             weight=50.0, height=100.0, address=f'hit')
    print(student)


def test_type_float_to_int():
    with pytest.raises(TypeError) as error:
        Student(name='李华1', age=1.1, phone=123456789,
                weight=50.0, height=100.0, address=f'hit',
                student_id=1)
    assert "实例化" in str(error.value)
    assert "类时," in str(error.value)


def test_check_type():
    students = [
        Student(name=f'李华{i}', age=i, phone=123456789,
                weight=50.0, height=100.0 + i, address=f'hit{i}')
        for i in range(1, 100)
    ]
    for student in students:
        print(student)


def test_no_default_value():
    student = Student(name=f'李华1', age=10, phone=123456789,
                      height=100.0, student_id=1)
    assert student.age == _parse_attr_value(student.age)
    assert student.weight == _parse_attr_value(student.weight)
    assert student.address == _parse_attr_value(student.address)


def test_change_position():
    @Entity(check_type=True)
    @dataclass
    class StudentChangePosition:
        name: str
        age: int = 10
        phone: int = d.not_null
        weight: float = d.not_null, 50.0
        height: float = d.not_null, d.unique
        address: str = d.not_null, 'hit', d.unique
        student_id: int = d.auto_primary_key

    student = StudentChangePosition(name=f'李华1', phone=123456789,
                                    height=100.0, student_id=1)
    assert student.age == _parse_attr_value(StudentChangePosition.age)
    assert student.weight == _parse_attr_value(StudentChangePosition.weight)
    assert student.address == _parse_attr_value(StudentChangePosition.address)


def test_multiple_default_value():
    @Entity(check_type=True)
    class StudentMultipleDefaultValue:
        name: str
        age: int = 10
        phone: int = d.not_null
        weight: float = d.not_null, 50.0
        height: float = d.not_null, d.unique
        address: tuple = d.not_null, 'hit', d.unique, 'hit'
        student_id: int = d.auto_primary_key

    student = StudentMultipleDefaultValue(name=f'李华1', phone=123456789,
                                          height=100.0, student_id=1)
    assert _parse_attr_value(student.address) == ('hit', 'hit')


def test_repeat_Define():
    @Entity(check_type=True)
    class StudentRepeatDefine:
        name: str
        age: int = 10
        phone: int = d.not_null
        weight: float = d.not_null, 50.0
        height: float = d.not_null, d.unique, d.unique
        address: str = d.not_null, 'hit', d.unique
        student_id: int = d.auto_primary_key

    student = StudentRepeatDefine(name=f'李华1', phone=123456789,
                                  height=100.0, student_id=1)


def test_None():
    @Entity(check_type=True)
    @dataclass
    class StudentNone:
        name: str
        age: int = None
        phone: int = d.not_null, None
        weight: float = None, d.not_null
        height: float = d.not_null, d.unique
        address: str = d.not_null, None, d.unique
        student_id: int = d.auto_primary_key

    student = StudentNone(name=f'李华1', height=100.0, student_id=1)
    assert student.age is None
    assert student.phone is None
    assert student.address is None
    assert student.height == 100.0


def test_type_bool():
    @Entity(check_type=True)
    @dataclass
    class Student:
        name: str
        if_18: bool
        contact_info: float
        student_id: int = d.auto_primary_key, d.comment('学生id')

    student = Student(name='李华', if_18=True, contact_info=123.0)


if __name__ == '__main__':
    pytest.main(["-v", __file__, "--log-cli-level=INFO"])
