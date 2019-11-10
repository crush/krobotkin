import os
import sqlite3 as sqlite

import krobotkin.db as db


class TestDB:
    @classmethod
    def setup_class(cls):
        self.db_name = 'test_db.sqlite'
        self.conn = sqlite.connect(self.db_name)

        with self.conn.cursor() as curs:
            db.init_db(curs)


    @classmethod
    def teardown_class(cls):
        self.conn.close()
        os.remove(self.db_name)


    def test_poll_simple_create_retrieve(self):
        assert True
