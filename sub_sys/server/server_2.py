import socket, sys, os, time, sqlite3, threading, datetime
import cPickle as pickle
from shark import Shark
from thread import *

HOST = 'localhost'      #HOST IP  
PORT = 5000             #Port used to listen for client
BUFFER_SIZE = 2048      #Max buffersize to recv 
online_sharks = {}      #Dist of all online uids

#------------------ SET UP -----------------------
#set up database 
messages_db = sqlite3.connect('messages.db',isolation_level=None)
messages_cursor = messages.db.cursor()
#SETUP SEQUENCE FOR MSG_ID 
#individual messages, delete on sent
messages_cursor.execute('''CREATE TABLE IF NOT EXISTS messages
        (msg_id INT PRIMARY KEY,
         time_sent TEXT NOT NULL,
         msg TEXT,
         author_uid TEXT NOT NULL,
         dest TEXT)''');

#set up socket for connection
#might need to make this a global? 
server_sock = socket.socket(socket.AFINET, socket.SOCK_STREAM)
#socket setup for connection                                            
server_sock.setsockpt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#binding socket                                                         
try:
    server_sock.bind((HOST, PORT))
except socket.error, msg:
    print "Bind failed. Error: " + str(msg[0]) + "\n"

#------------------ END SETUP --------------------------  

""" Recive command from client through given socket
    parse recived command by ':'                     
    return as a list with command in [0] and args in [1:]      
"""
def recv_from_client(sock):
    recv_data = sock.recv(BUFFER_SIZE)
    parsed_data = rdata.split(':')
    print "received data: " + recv_data
    return parsed_data
#end recv_from_client                              

""" Takes args from client_thread                         
    compose message row and either send msg or insert into database.  
    ARGS = AUTHOR_ID : MSG : UID/TAG : DESG_UID/TAG                
"""
def write_message(sock, args):
    if len(args) < 4:
        fail = "FAIL:NOT_ENOUGH_ARGS"
        return fail
    dest_uid = None
    dest_tag = None
	#setup row info to insert                              
        author = args[0]
        msg = args[1]
        sent_time = datetime.datetime.now()
        if args[2] == "UID":
            dest_uid = args[3]
        elif args[2] == "TAG":
            dest_tag = args[3]
        else:
            fail = "FAIL:INVALID_UID_OR_TAG"
            return fail

""" Main client thread                                      
    recv data from client with recv_from_client and parase command   
    execute functs according to commands                              
    List of Commands:                                                 
      #GET_TORRENTS                                                 
      WRITE_MESSAGE                                                    
      #EDIT_SUB                                                        
      #EDIT_GROUP                                                      
"""
def client_thread(c_sock):
    #check for current client's uid
    while True:
        data = recv_from_client(c_sock)
        command = data[0]
        data = data[1:]

        send_data = None #initalize and reset after each iteration of loop                                                                      
        #GET_TORRENT:QUERY_TYPE:QUERY                                  
       	#no longer doing server side torrent db                        
       	#if command == "GET_TORRENT":           
        #WRITE_MESSAGE:AUTHOR_UID:MSG:UID/TAG:DEST_UID/TAG             
        if command == "WRITE_MESSAGE":
            #return success or fail                                    
            send_data = write_message(c_sock,data)
        #LOG_OFF                                                       
        elif command == "LOG_OFF":
            break
        else:
            send_data = "FAILED:INVALID_COMMAND"

        #send back to client if functions execute correctly            
        if send_data is not None:
            c_sock.send(send_data)
        #end_while_loop                                                

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
        client_sock, addr = server_socket.accept()

        print "Connection established with " + addr[0] + ":" + str(addr[1])
        #get uid                                                       
        recv_from_client(client_sock)
        #keep track of who is online                                   
        #for messaging purposes                                        
        online_sharks.update({client_sock})
        start_new_thread(client_thread, (client_sock,))
        time.sleep(2)
    #end process funct                                                  


if __name__ == "__main__":
    #start a separate daemon xthread to listen for client connections  
    thread = threading.Thread(target=process)
    thread.daemon = True
    thread.start()

    #won't quit until server admin enter "Quit"                        
    while True:
        server_command = raw_input("\t>")
        if server_command == "Quit":
            break
    print "Closing down server..."
    server_sock.close()
