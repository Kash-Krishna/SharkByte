import socket, sys, os, time, sqlite3, threading, datetime
import cPickle as pickle
from thread import *

HOST = 'localhost'    #HOST IP
PORT = 5000           #Port used to listen for client
BUFFER_SIZE = 8000    #Max buffersize to recv
online_sharks = {}    #List of all online uids
#TOD: MAKE SERVER_LOG.TXT
#------------------ SET UP -----------------------
#set up database
messages_db = sqlite3.connect('messages.db',isolation_level=None)
messages_cursor = messages_db.cursor()
#SETUP SEQUENCE FOR MSG_ID
#individual messages, delete on sent
messages_cursor.execute('''CREATE TABLE IF NOT EXISTS messages
        (msg_id INT PRIMARY KEY AUTOINCREMENT,
         time_sent TEXT NOT NULL,
         msg TEXT,
         author_uid TEXT NOT NULL,
         dest TEXT)''');
#------------------ END SETUP --------------------------


""" Recive command from client through given socket
    parse recived command by ':'
    return as a list with command in [0] and args in [1:]
"""
def recv_from_client(sock):
    try:
        recv_data = sock.recv(BUFFER_SIZE)
    except socket.error, msg:
        log.write("Error: " + str(msg[0]) + '\n')
        return None
    parsed_data = recv_data.split(':')
    log.write("received data: " + recv_data + '\n')
    return parsed_data 
#end recv_from_client

""" Takes args from client_thread
    compose message row and either send msg or insert into database.
    ARGS = AUTHOR_ID : MSG : DESG_UID/TAG
"""
def write_message(sock, args, msg_db):
    
    if len(args) < 3:
        fail = "FAIL:NOT_ENOUGH_ARGS"
        return fail

    #setup row info to insert
    author = args[0].strip()
    msg = args[1].strip()
    sent_time = datetime.datetime.now()
    dest = args[2].strip()
    msg_id = None
    #determine to either send or insert            
    msg_row = (sent_time, msg, author, dest)
    #if dest_uid in dict online_sharks then send
    if dest in online_sharks:
        jar = pickle.dumps(msg_row)
        online_sharks[dest].send(jar)
        success = "SUCCESS:MESSAGE_SENT"
    else:
        #add NULL for first column
        insert_row = (msg_id, sent_time, msg, author, dest)
        msg_db.execute('''INSERT INTO messages VALUES (?,?,?,?,?)''', insert_row);
        success = "SUCCESS:MESSAGE_SENT"
    return success
#end write_message(sock, args)

""" look into message.db and send any Q'd messages
"""
def send_offline_msg(sock, uid, sub_list, msg_db):
    msg_db.execute('''SELECT * FROM messages WHERE dest=\'''' + uid + '\'');
    msgs_to_send = msg_db.fetchall()
    for sub in sub_list:
        msg_db.execute('''SELECT * FROM messages WHERE dest=\'''' + sub + '\'');
        temp_list = msg_db.fetchall()
        msgs_to_send = msgs_to_send + temp_list
    print msgs_to_send
    jar = pickle.dumps(msgs_to_send)
    sock.send(jar)
    msg_db.execute('''DELETE FROM messages WHERE dest=\''''+ uid + '\'');
#end send_offline_msg

""" Main client thread
    recv data from client with recv_from_client and parase command
    execute functs according to commands
      WRITE_MESSAGE
      LOG_OFF
"""
def client_thread(c_sock,uid):
    #check for current client's uid
    while True:
        data = recv_from_client(c_sock)
        #data = c_sock.recv(BUFFER_SIZE)
        command = data[0]
        data = data[1:]
        
        send_data = None #initalize and reset after each iteration of loop
        #WRITE_MESSAGE:AUTHOR_UID:MSG:UID/TAG:DEST_UID/TAG
        if command == "WRITE_MESSAGE":
            #return success or fail
            messages_db = sqlite3.connect('messages.db',isolation_level=None)
            messages_cursor = messages_db.cursor()
            send_data = write_message(c_sock,data,messages_cursor)
            log.write("in client thread: " + send_data + '\n')
        #LOG_OFF
        elif command == "LOG_OFF":
            break
        else:
            log.write("FAILED:INVALID_COMMAND\n")
                        
        #send back to client if functions execute correctly
        if send_data is not None:
            try:
                c_sock.send(send_data)
            except socket.error, msg:
                log.write("Error: " + str(msg[0]))
        #end_while_loop
        log.write("------------------------------------\n")
    #client exiting //going offline
    c_sock.send("Closing connection...")
    #remove user from online users
    #FIXME
    if shark in online_sharks:
        online_sharks.remove(shark)
    c_sock.close()
    return
#end client_thread(c_sock)

""" Process to listen on server_socket
    start a new thread with funct client_thread
"""
def process():
    while True:
        client_sock, addr = server_sock.accept()
        log.write("Connection established with " + addr[0] + ":" + str(addr[1]) + '\n')
        msg_db = sqlite3.connect('messages.db',isolation_level=None)
        msg_cursor = msg_db.cursor()
        #get uid coordinating
        r_data_uid = pickle.loads(client_sock.recv(BUFFER_SIZE))
        uid = r_data_uid[1].rstrip()
        sub_list = r_data_uid[2]
        send_offline_msg(client_sock, uid, sub_list, msg_cursor)
        time.sleep(1)
        #keep track of who is online
        #for messaging purposes
        online_sharks.update({uid : client_sock})
        start_new_thread(client_thread, (client_sock,uid))
        time.sleep(2)
    #end process funct

if __name__ == "__main__":
    #set up socket for connection
    global server_sock 
    log = open('server_log.txt', 'w')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket setup for connection
    server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    
    #binding socket
    try:
        server_sock.bind((HOST, PORT))
    except socket.error, msg:
        log.write("Bind failed. Error: " + str(msg[0]) + "\n")
    server_sock.listen(10)
    
    #start a separate daemon xthread to listen for client connections
    thread = threading.Thread(target=process)
    thread.daemon = True
    thread.start()

    #won't quit until server admin enter "Quit"
    while True:
        server_command = raw_input("\t>")
        if server_command == "Quit":
            break
    log.write("Closing down server...\n")
    log.close()
    server_sock.close()
    
