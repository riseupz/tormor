import pytest
from tormor.schema import (
    migrate,
    _get_schema_files_path,
    find_schema_paths,
    SchemaFilesNotFound,
    enablemodules,
)
from tormor.connection import Connection

import os
import psycopg2

# def test_should_migrate_sucessfully():
#     assert 1 == 2


def test_schema_path_should_come_from_os_environments():
    os.environ["SCHEMA_PATH"] = 'test_path:test_path_2'
    actual = _get_schema_files_path()
    os.environ.pop("SCHEMA_PATH")

    assert actual == ['test_path', 'test_path_2']


def test_schema_path_should_come_from_relative_path_when_no_os_shcema_path_is_set():
    os.environ["SCHEMA_PATH"] = ""
    actual = _get_schema_files_path()[0].split('/')
    expect = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Schema").split('/')
    expect[7] = 'tormor'
    os.environ.pop("SCHEMA_PATH")

    assert actual == expect


def test_should_return_error_when_there_is_no_schema_path():
    with pytest.raises(SchemaFilesNotFound):
        find_schema_paths('')


def test_module_is_saved_into_database_when_run_enable_module():
    os.environ["SCHEMA_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    cnx = Connection('user=sem')
    enablemodules(cnx, 'module_1')
    cnx.commit()
    print('1')
    assert 2 == 1


# def test_should_re
# find_schema_paths
