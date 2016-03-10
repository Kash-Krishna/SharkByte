
import sqlite3

class db_interface():

    def __init__(self):
        self.conn = sqlite3.connect("/root/Desktop/Deluge/youtor/sub_sys/client/torrents.db")
        self.c = self.conn.cursor()
        self.TABLE = "torrents"

    def get_all_columns(self):
        self.c.execute("SELECT * FROM torrents ORDER BY seeders")
        return self.c.fetchall()

    def find_by_filter(self, column, query):
        self.c.execute("SELECT * FROM torrents WHERE " + column + " LIKE '%" + query + "%'")
        return self.c.fetchall()

