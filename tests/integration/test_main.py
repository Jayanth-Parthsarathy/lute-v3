"""
Test main entry point.
"""

import os
import sqlite3
from contextlib import closing

from lute.main import init_db_and_app


def test_init_no_existing_database(testconfig):
    """
    If no db exists, init should:
    - do the db setup
    - create the flask app
    """
    if os.path.exists(testconfig.dbfilename):
        os.unlink(testconfig.dbfilename)

    app = init_db_and_app(testconfig)

    assert os.path.exists(testconfig.dbfilename) is True, 'db exists'
    assert testconfig.dbname.startswith('test_')

    def assert_tables_exist(msg: str):
        with closing(sqlite3.connect(testconfig.dbfilename)) as conn:
            cur = conn.cursor()
            sql = """SELECT name FROM sqlite_master
            WHERE type='table' AND name in ('words', 'languages')
            order by name;"""
            tnames = cur.execute(sql).fetchall()
            tnames = [t[0] for t in tnames]
            assert tnames == [ 'languages', 'words' ], msg
    assert_tables_exist('db set up correctly')

    client = app.test_client()
    response = client.get('/')
    assert b'Lute' in response.data