import socket, sys, os, time, sqlite3, subprocess, datetime
import cPickle as pickle
from thread import *
#change crawler db path

HOST = 'localhost' #change to server ip
PORT = 5000        #change to port used by server
BUFFER_SIZE = 8000

""" Print out the menu
    ask users one to pick an option U, E, S
    U: update the torrent //query server db
    E: Edit Subscription //add or drop
    T: Follow or unfollow a group tag
    S: Send a message // to uid or 
"""
def menu():
    while 1:
        print "Send a Message\t\t\t(S)"
        print "Quit\t\t\t\t(Q)"
        option = raw_input()
        if option == "S" or option == "Q":
            return option
        else:
            print "Invalid option!"

""" Retrieve Q'd Messages from server
    send server "RETRIEVE:UID:TAGS"
    INSERT all msg into msg.db
"""
def retrieve_messages(sock, uid, tags, message_db):
    #RETRIEVE, UID, LIST_OF_TAGS
    command = ("RETRIEVE", uid, tags)
    jar = pickle.dumps(command)
    sock.send(jar)
    data = pickle.loads(sock.recv(BUFFER_SIZE))
    for d in data:
        print d
        message_db.execute('''INSERT OR IGNORE INTO messages VALUES(?,?,?,?,?)''', d)
    
#end retrieve_messages


""" Daemon Thread running in background for crawler
    running update_loots once user log on
    check for 30 min difference of time.
    re run crawler if > 30min
"""
def crawler_thread(sub_list, torrent_db):
    start_time = datetime.datetime.now()
    while True:
        time_now = datetime.datetime.now()
        time_diff = start_time - time_now
        if time_diff > datetime.timedelta(minutes=30) or time_diff < datetime.timedelta(seconds=5):
            update_loots(sub_list, torrent_db)

#end crawler_thread()
   
""" Send 'Get_Torrents' as command to server
    insert list of recv data into torrent db
    run this funct in a separate thread. checking every 30min for a re-run
"""
def update_loots(sub_list, torrent_db):
    #go through sub_list
    print "getting sweet loots!"
    for sub in sub_list:
        command = "python crawler.py kat " + sub
        proc = subprocess.Popen(command,shell=True)
        #proc = subprocess.Popen("sudo python ~/sharkByte/web_crawler/crawler.py kat "+sub, shell=True)
        proc.wait()
    return

""" Send 'Write_Message' as command to server
    insert message to 'message_db'
    recv message status from server
    reprompt user if failed
"""
def write_message(sock, uid, message_db):
    msg = ""
    time_sent = datetime.datetime.now()
    tag_or_id = ""
    msg_id_col = None
    #ping server time
    #send to uid/tag
    tag_or_uid = raw_input("Send Message to: ")
    #prompt user for message
    msg = raw_input("Message to send: ")
    #send to server
    command = "WRITE_MESSAGE:" + uid + ":" + msg + ":" + tag_or_uid
    sock.send(command)
    data = sock.recv(BUFFER_SIZE)
    p_data = data.split(":")
    if p_data[0] == "SUCCESS":
        #INSERT INTO MESSAGE DB
        insert_row = (msg_id_col, time_sent, msg, uid, tag_or_uid)
        message_db.execute('''INSERT OR IGNORE INTO messages VALUES(?,?,?,?,?)''', insert_row);
        print p_data[0] + " " + p_data[1] + '\n'
        return
    else:
        print "ERROR: Fail to send message"
        return

def get_sub_list():
    #read from subl_list.txt for list of subs
    sub_list = []
    #CHANGE ABS PATH
    #with open("~/Desktop/Deluge/youtor/deluge/scripts/subscription/subscription/data/sub.txt") as f_sub:
    with open("sub_list.txt") as f_sub:
        temp_sub = f_sub.readlines()
    #get rid of '\n'
    #get "Names:" only
    for s in temp_sub:
        if "Name: " in s:
            s = s[6:]
            s = s.replace(" ", "%20")
            sub_list.append(s.strip())
        
    return sub_list

def get_group_tags():
    #read from group_tags.txt for listof groups 
    group_tags = []
    with open("group_tags.txt") as f_tag:
        temp_tags = f_tag.readlines()
    #get rid of '\n'
    for t in temp_tags:
        group_tags.append(t.strip())
    return group_tags

if __name__ == "__main__":
    #socket setup
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.settimeout(10)
    
    #create connection to server
    try:
        server_sock.connect((HOST,PORT))
    except:
        print "Failure to connect to HOST at PORT " + str(PORT)
        #sys.exit()
    
    #SETUP
    print "Initilizing..."
    #read from uid.txt
    uid_text = open("uid.txt")
    uid = uid_text.read()
    #get subscription list from text file
    #get group tags from text file
    sub_list = get_sub_list()
    group_tags = get_group_tags()
    
    #create client side tables in db, use IF NOT EXISTS
    #set up messages db
    messages_db = sqlite3.connect('messages.db',isolation_level=None)
    messages_cursor = messages_db.cursor()
    #look into SEQUENCES
    messages_cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
            (msg_id INT PRIMARY KEY,
             time_sent TEXT NOT NULL,
             msg TEXT, 
             author_uid TEXT NOT NULL, 
             tag TEXT);''')
    
    #set up torrents db. 
    torrents_db = sqlite3.connect('torrents.db',isolation_level=None)
    torrents_cursor = torrents_db.cursor()
    torrents_cursor.execute('''CREATE TABLE IF NOT EXISTS torrents
            (torrent_name TEXT,
             file_size REAL,
             seeders INT,
             leechers INT,
             uploader TEXT,
             upload_date_and_time TEXT,
             magnet_link TEXT PRIMARY KEY NOT NULL);''')
    #retrieve any Q'd Messages
    retrieve_messages(server_sock,uid,group_tags, messages_cursor)
    #run crawler thread in daemon thread
    thread = start_new_thread(crawler_thread,(sub_list, torrents_cursor))
    #start main loop
    while True:
        option = menu()
        if option == "S": #write a message to send
            write_message(server_sock, uid, messages_cursor)
        elif option == "Q": #quit client 
            sys.exit()
    os.waitpid()
    #exiting main
