
import sqlite3

class db_interface():

    def __init__(self):
        self.conn = sqlite3.connect("/root/Desktop/Deluge/youtor/web_crawler/youtor.db")
        self.c = self.conn.cursor()
        self.TABLE = "local_youtor"

    def get_all_columns(self):
        self.c.execute("SELECT * FROM local_youtor ORDER BY seeders")
        return self.c.fetchall()

    def find_by_filter(self, column, query):
        self.c.execute("SELECT * FROM local_youtor WHERE " + column + " LIKE '%" + query + "%'")
        return self.c.fetchall()

