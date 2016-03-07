import socket, sys, os, time, sqlite3
from shark import Shark #sharks are users
from thread import *

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 2048

def send_to_server():
    skip

"""Print out the menu
   ask users one to pick an option U, E, S
   U: update the torrent //query server db
   E: Edit Subscription //add or drop
   T: Follow or unfollow a group tag
   S: Send a message // to uid or 
"""
def menu():
    while 1:
        print "Update Torrent list\t\t(U)"
        print "Edit Subscription\t\t(E)"
        print "Follow or unfollow Shivers\t(F)"
        print "Send a Message\t\t\t(S)"
        option = raw_input()
        if option == "U" or option == "E" or option == "S":
            return option
        else:
            print "Invalid option!"

def update_loots(sock,uid):
    command = "GET_TORRENTS:" + uid
    sock.send(command)
    rdata = pickle.loads(sock.recv(BUFFER_SIZE))
    skip

if __name__ == "__main__":
    """
    #socket setup
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.settimeout(10)
    
    #create connection to server
    try:
        server_sock.connect((HOST,PORT))
    except:
        print "Failure to connect to HOST at PORT " + str(PORT)
        sys.exit()
    """
    #SETUP
    print "Initilizing..."
    #read from uid.txt
    uid_text = open("uid.txt")
    uid = uid_text.read()
    #validate uid
    
    #read from subl_list.txt for list of subs
    sub_list = []
    with open("sub_list.txt") as f_sub:
        temp_sub = f_sub.readlines()
    #get rid of '\n'
    for s in temp_sub:
        sub_list.append(s.strip())
    
    #read from group_tags.txt for listof groups 
    group_tags = []
    with open("group_tags.txt") as f_tag:
        temp_tags = f_tag.readlines()
    #get rid of '\n'
    for t in temp_tags:
        group_tags.append(t.strip())

    #create client side tables in db, use IF NOT EXISTS
    messages_db = sqlite3.connect('messages.db')
    message_cursor = messages_db.cursor()
    while True:
        option = menu()
        
        break
        
    
