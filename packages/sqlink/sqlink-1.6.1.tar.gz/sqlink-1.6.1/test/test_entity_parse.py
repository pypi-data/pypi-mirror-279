# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from sqlink.entity import _parse_attr_value, _parse_defines, Entity, Define as d, _Define


@Entity
@dataclass
class Student:
    attr_int: int
    attr_float: float
    attr_bool: bool
    attr_str: str

    attr_tuple: tuple
    attr_list = list
    attr_dict = dict
    attr_set = set

    attr_int_default: int = 1
    attr_float_default: float = 1.0
    attr_bool_default: bool = True
    attr_str_default: str = '1'

    attr_1d: str = d.not_null
    attr_2d: str = d.not_null, d.unique
    attr_3d: str = d.not_null, d.unique, d.primary_key

    attr_str_and_d: str = '1', d.not_null, d.datatype("varchar(200)")
    attr_int_and_d: int = 1, d.not_null
    attr_float_and_d: float = 1.0, d.not_null
    attr_bool_and_d: bool = True, d.not_null

    attr_str_and_2d: str = '1', d.not_null, d.unique, d.datatype("varchar(200)")
    attr_int_and_2d: int = 1, d.not_null, d.unique
    attr_float_and_2d: float = 1.0, d.not_null, d.unique
    attr_bool_and_2d: bool = True, d.not_null, d.unique

    id: int = d.auto_primary_key

    attr_tuple_c: tuple = d.ignore
    attr_list_c: list = d.ignore
    attr_dict_c: dict = d.ignore
    attr_set_c: set = d.ignore

    attr_tuple_c_and_v: tuple = d.ignore, (1,)
    attr_tuple2_c_and_v: tuple = d.ignore, 1, 2
    attr_list_c_and_v: list = d.ignore, [1]
    attr_dict_c_and_v: dict = d.ignore, {'1': 1}
    attr_set_c_and_v: set = d.ignore, {1}


# ====================================================================================================================
def test_parse_1value():
    assert Student.attr_int_default == _parse_attr_value(Student.attr_int_default)
    assert Student.attr_float_default == _parse_attr_value(Student.attr_float_default)
    assert Student.attr_bool_default == _parse_attr_value(Student.attr_bool_default)
    assert Student.attr_str_default == _parse_attr_value(Student.attr_str_default)


def test_parse_1v_from_1c():
    assert Student.attr_int_default == _parse_attr_value(Student.attr_int_and_d)
    assert Student.attr_float_default == _parse_attr_value(Student.attr_float_and_d)
    assert Student.attr_bool_default == _parse_attr_value(Student.attr_bool_and_d)
    assert Student.attr_str_default == _parse_attr_value(Student.attr_str_and_d)


def test_parse_1v_from_2c():
    assert Student.attr_int_default == _parse_attr_value(Student.attr_int_and_2d)
    assert Student.attr_float_default == _parse_attr_value(Student.attr_float_and_2d)
    assert Student.attr_bool_default == _parse_attr_value(Student.attr_bool_and_2d)
    assert Student.attr_str_default == _parse_attr_value(Student.attr_str_and_2d)


def test_parse_1define():
    assert isinstance(Student.attr_1d, _Define)
    assert _parse_defines(Student.attr_1d) == [d.not_null]
    assert _parse_defines(Student.id) == [d.auto_primary_key]


def test_parse_2c():
    defines = {d.not_null, d.unique}
    assert set(_parse_defines(Student.attr_2d)) == defines


def test_parse_3c():
    defines = {d.not_null, d.unique, d.primary_key}
    assert set(_parse_defines(Student.attr_3d)) == defines


def test_parse_value_from_c_no_default():
    assert _parse_attr_value(Student.attr_1d) is None
    assert _parse_attr_value(Student.attr_2d) is None
    assert _parse_attr_value(Student.attr_3d) is None


def test_parse_1c_from_1v():
    assert _parse_defines(Student.attr_str_and_d) == [d.not_null, d.datatype("varchar(200)")]
    assert _parse_defines(Student.attr_int_and_d) == [d.not_null]
    assert _parse_defines(Student.attr_bool_and_d) == [d.not_null]
    assert _parse_defines(Student.attr_float_and_d) == [d.not_null]


def test_parse_2c_from_1v():
    defines = {d.not_null, d.unique}
    assert set(_parse_defines(Student.attr_str_and_2d)) == {d.not_null, d.unique, d.datatype("varchar(200)")}
    assert set(_parse_defines(Student.attr_int_and_2d)) == defines
    assert set(_parse_defines(Student.attr_bool_and_2d)) == defines
    assert set(_parse_defines(Student.attr_float_and_2d)) == defines


def test_parse_ignore_define():
    assert _parse_defines(Student.attr_tuple_c) == [d.ignore]
    assert _parse_defines(Student.attr_list_c) == [d.ignore]
    assert _parse_defines(Student.attr_dict_c) == [d.ignore]
    assert _parse_defines(Student.attr_set_c) == [d.ignore]


def test_parse_ignore_value():
    assert _parse_attr_value(Student.attr_tuple_c_and_v) == (1,)
    assert _parse_attr_value(Student.attr_tuple2_c_and_v) == (1, 2)
    assert _parse_attr_value(Student.attr_list_c_and_v) == [1]
    assert _parse_attr_value(Student.attr_dict_c_and_v) == {'1': 1}
    assert _parse_attr_value(Student.attr_set_c_and_v) == {1}


def test_parse_ignore_value_no_default():
    assert _parse_attr_value(Student.attr_tuple_c) is None
    assert _parse_attr_value(Student.attr_list_c) is None
    assert _parse_attr_value(Student.attr_dict_c) is None
    assert _parse_attr_value(Student.attr_set_c) is None


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
