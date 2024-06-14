# -*- coding:utf-8 -*-
import os

import pytest

if __name__ == "__main__":
    os.environ['DB_IMPL'] = 'sqlite'
    print("Running tests with SqliteDatabase...")
    pytest.main([".", "-vv", "--ignore=test_env.py"])
    # 清除环境变量，以防对其他进程产生影响
    del os.environ['DB_IMPL']

    # os.environ['DB_IMPL'] = 'mysql'
    # print("\nRunning tests with MysqlMetaDatabase...")
    # pytest.main([".", "-vv", "--ignore=test_env.py"])
    # # 清除环境变量
    # del os.environ['DB_IMPL']
