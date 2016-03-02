import socket, sys, os, time, sqlite3
from shark import Shark #sharks are users
from thread import *

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

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

def update_loots(sock):
    

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
    #read from subl_list.txt for list of subs
    subl_text = open("sub_list.txt")
    sub_list = subl_text.read()
    #read from group_tags.txt for listof groups 
    gtags_text = open("group_tags.txt")
    group_tags = gtags_text.read()
    
    #create client side tables in db, use IF NOT EXISTS
    #wait...
    while True:
        option = menu()
        
        break
        
    
