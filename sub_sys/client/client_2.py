import socket, sys, os, time, sqlite3, subprocess
from shark import Shark #sharks are users 
#move crawler dir(?)
#add path
#change crawler db path

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 2048

""" Send command to server through socket
    returns recv'd data parsed into a list
"""
def send_to_server(command, sock):
    jar = pickle.dumps(command)
    sock.send(jar)
    rdata = pickle.loads(sock.recv(BUFFER_SIZE))
    #parse rdata into list
    return rdata

""" Print out the menu
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
        print "Quit\t\t\t\t(Q)"
        option = raw_input()
        if option == "U" or option == "E" or option == "S" or option == "Q":
            return option
        else:
            print "Invalid option!"
""" Retrieve Q'd Messages from server
    send server "RETRIEVE:UID:TAGS"
    INSERT all msg into msg.db
"""
def retrieve_messages(sock, uid, tags):

    command = ("RETRIEVE", uid, tags)
    send
#end retrieve_messages

""" Send 'Get_Torrents' as command to server
    insert list of recv data into torrent db
"""
def update_loots(sock, sub_list, torrent_db):
    #go through sub_list
    for sub in sub_list:
        proc = Popen("python ./webcrawler/crawler kat " + sub)
        proc.wait()

    return

""" Send 'Write_Message' as command to server
    insert message to 'message_db'
    recv message status from server
    reprompt user if failed
"""
def write_message(sock, uid, message_db):
    msg = ""
    time_sent = ""
    tag_or_id = ""
    #ping server time
    #send to uid/tag
    tag_or_uid = raw_input("Send Message to: ")
    #prompt user for message
    msg = raw_input("Message to send: ")
    #send to server
    command = "WRITE_MESSAGE:" + msg + ":" + uid + ":" + tag_or_id
    data = send_to_server(command, sock)
    if data

def get_sub_list():
    #read from subl_list.txt for list of subs
    sub_list = []
    with open("sub_list.txt") as f_sub:
        temp_sub = f_sub.readlines()
    #get rid of '\n'
    for s in temp_sub:
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
    #validate uid (?)

    #get subscription list from text file
    #get group tags from text file 
    sub_list = get_sub_list()
    group_tags = get_group_tags()

    #create client side tables in db, use IF NOT EXISTS
    #set up messages db                         

