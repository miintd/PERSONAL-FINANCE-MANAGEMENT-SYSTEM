# database.py
import mysql.connector
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def call_procedure(self, proc_name, args=()):
        self.cursor.callproc(proc_name, args)
        self.conn.commit()
        for result in self.cursor.stored_results():
            return result.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()