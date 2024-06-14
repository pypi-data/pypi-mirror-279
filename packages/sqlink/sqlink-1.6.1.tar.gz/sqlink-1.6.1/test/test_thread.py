import os
import threading
from dataclasses import dataclass

import pytest

from sqlink import Entity, Define as d, Dao, DaoFunc, Sql
from sqlink.database import DB, DBFunc


@Entity
@dataclass
class Student:
    name: str
    student_id: int = d.auto_primary_key


@Dao(Student)
class DaoStudent(DaoFunc):
    @Sql("select * from __;", fetch_type=Student)
    def select_all(self):
        pass


@DB
class Database(DBFunc):
    dao_student = DaoStudent()


# ====================================================================================================================
def generate_students(start, end):
    return [Student(name=f'李华{i}', student_id=i) for i in range(start, end)]


def insert_data(db: Database, num=100):
    students = generate_students(0, num)
    db.dao_student.insert(students)
    db.commit()
    return students


def get_test_db_path(db_name):
    func_path = __file__
    db_path = os.path.join(os.path.dirname(func_path), f"test_db\\{db_name}.db")
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    return db_path


def get_db(db_name):
    db = Database()
    db.connect(f"sqlite://{get_test_db_path(db_name)}", check_same_thread=False)
    return db


# ====================================================================================================================
def test_multiple_init_and_use():
    db_name = 'same_thread'
    db_path = get_test_db_path(db_name)
    if os.path.exists(db_path):
        os.remove(db_path)
    db = get_db(db_name)
    db.create_tables()
    students = insert_data(db, 100)

    def query():
        temp_db = get_db(db_name)
        result = temp_db.dao_student.select_all()
        assert result == students

    for _ in range(10):
        query()


def test_multiple_init_in_thread():
    db_name = 'multiple_thread'
    db_path = get_test_db_path(db_name)
    if os.path.exists(db_path):
        os.remove(db_path)
    db = get_db(db_name)
    db.create_tables()
    students = insert_data(db, 100)

    def query():
        temp_db = get_db(db_name)
        result = temp_db.dao_student.select_all()
        assert result == students

    for _ in range(10):
        task = threading.Thread(target=query)
        task.start()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
