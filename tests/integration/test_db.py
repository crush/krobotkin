import os
import sqlite3 as sqlite

import krobotkin.db as db
import krobotkin.polls as polls


class TestDB:
    @classmethod
    def setup_class(cls):
        cls.db_name = 'test_db.sqlite'
        cls.conn = sqlite.connect(cls.db_name)

        curs = cls.conn.cursor()
        db.init_db(curs)
        curs.commit()


    @classmethod
    def teardown_class(cls):
        cls.conn.close()
        os.remove(cls.db_name)


    def test_poll_simple_create_retrieve(self):
        p = polls.Poll('test', ['test1', 'test2'], [])

        c = self.conn.cursor()
        store = store_fn(c)
        retr = fetch_fn(c)
        pid = store(db.NULL, p)
        p2 = retr(pid)
        c.commit()

        assert p2.question == p.question
        assert p2.options == p.options
