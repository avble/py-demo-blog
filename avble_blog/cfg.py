import os
from os.path import dirname


def get_cfg(key, default_value):
    mod_path = dirname(__file__)
    return os.getenv(key, f'{mod_path}/{default_value}')

g_cfg = {
    'db_cfg':{
        "name": get_cfg("DB_NAME", "blog.db"),
        "schema": get_cfg("DB_SCHEMA", "db/schema.sql"),
        "test_data": get_cfg("DB_TEST_DATA", 'cfg/test_data.sql')
    }
}