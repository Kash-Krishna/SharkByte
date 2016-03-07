
import sqlite3
"""
conn = sqlite3.connect("../../../../web_crawler/youtor.db")

c = conn.cursor()

for row in c.execute("SELECT * FROM local_youtor"):
    print row[0]
"""

class db_interface():

    def __init__(self):
        self.conn = sqlite3.connect("../../../../web_crawler/youtor.db")
        self.c = self.conn.cursor()
        self.TABLE = ("local_youtor",)

    def get_all_columns(self):
        self.c.execute("SELECT * FROM local_youtor")
        return self.c.fetchall()

    def find_by_name(self, name):
        self.c.execute("SELECT * FROM ? WHERE torrent_name=?", self.TABLE, name)
        return self.c.fetchall()

    

    
    
