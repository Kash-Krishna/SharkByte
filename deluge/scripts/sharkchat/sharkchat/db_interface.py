
import sqlite3

class db_interface():

    def __init__(self):
        self.conn = sqlite3.connect("/home/rlaw/Documents/cs179_kash/youtor/sub_sys/client/messages.db")
        # self.conn = sqlite3.connect("/root/Desktop/Deluge/youtor/sub_sys/client/torrents.db")
        self.c = self.conn.cursor()
        self.TABLE = "messages"

    def get_new_columns(self, last_update_time, now):
        # figure out how to compare datetime objects ... put into strings and see how sql wants it
        # self.c.execute("SELECT * FROM messages WHERE " + last_update_time + " < " + now)
        # self.c.execute("SELECT * FROM messages2 where 'time' <" + "\'" + now + "\'")
        self.c.execute("SELECT * FROM messages")
        result = self.c.fetchall()
        self.conn.close()
        return result

    def insert_new_message(self, msgid, message_text, to_user_id, from_user_id, time):     
        q = ("INSERT INTO messages VALUES(\'" + msgid + "\', \'" + time + "\', \'" + message_text + "\', \'" + from_user_id + "\', \'" + to_user_id + "\')")
        print q
        self.c.execute(q)
        self.conn.commit()
        result = self.c.fetchall()
        self.conn.close()
        return result

