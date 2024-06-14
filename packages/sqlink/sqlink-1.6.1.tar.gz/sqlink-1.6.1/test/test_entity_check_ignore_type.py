from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d


def test_entity_check_ignore_type():
    @Entity(check_type=True)
    @dataclass
    class Student:
        name: str
        score: list

    with pytest.raises(TypeError) as error:
        Student('1', 1)
    assert "实例化" in str(error.value)
    assert "类时," in str(error.value)

    @Entity(check_type=True)
    @dataclass
    class Student2:
        name: str
        score: list = d.ignore

    Student2('1', 1)


if __name__ == '__main__':
    pytest.main(["-v", __file__, "--log-cli-level=INFO"])
