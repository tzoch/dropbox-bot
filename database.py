#! usr/bin/python
'''
Class to handle database connections and queries for 
Dropbox Mirror Bot
'''

import sqlite3

class Database(object):

    def __init__(self, database=":memory:"):
        self._database = database
        c = self.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS dropbox_submissions (
                   processed_id INTEGER PRIMARY KEY ASC,
                   submission_id VARCHAR(10) UNIQUE)')
        self.conn.commit()

    @property
    def conn(self):
        if not hasattr(self, '_connection'):
            self_connection = sqlite3.connect(self.database)
        return self._connection

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def is_processed(self, submission_id):
    '''Return true if the submission has already been processed'''
        c = self.cursor()
        c.execute('SELECT submission_id FROM dropbox_submissions WHERE
                   submission_id = ?', (submission_id,))
        if c.fetchone():
            return True
        return False

    def mark_as_processed(self, submission_id):
        c = self.cursor()
        c.execute('INSERT INTO dropbox_submissions (submission_id) VALUES (?)'
                  , (submission_id,))
        self.conn.commit()

