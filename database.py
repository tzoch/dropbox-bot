#! usr/bin/python
'''
Class to handle database connections and queries for 
Dropbox Mirror Bot
'''

import sqlite3

from utils import generate_thing_ids

class Database(object):

    def __init__(self, database=":memory:"):
        self._database = database
        c = self.cursor()
        query = '''CREATE TABLE IF NOT EXISTS dropbox_submissions (
                   processed_id INTEGER PRIMARY KEY ASC,
                   submission_id VARCHAR(10) UNIQUE)'''
        c.execute(query)
        self.conn.commit()

    @property
    def conn(self):
        if not hasattr(self, '_connection'):
            self._connection = sqlite3.connect(self._database)
        return self._connection

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def is_processed(self, submission_id):
        '''Return true if the submission has already been processed'''
        
        c = self.cursor()
        query = '''SELECT submission_id FROM dropbox_submissions 
                   WHERE submission_id = (?)'''

        c.execute(query, (submission_id,))
        if c.fetchone():
            return True
        return False

    def mark_as_processed(self, submission_id):
        c = self.cursor()
        query = '''INSERT INTO dropbox_submissions (submission_id) 
                   VALUES (?)'''
        c.execute(query , (submission_id,))
        self.conn.commit()

if __name__ == '__main__':
    pass
# Add some random thing_ids for testing 
#
#    db = Database('processed.db')
#    for thing_id in generate_thing_ids(10):
#        db.mark_as_processed(thing_id)
