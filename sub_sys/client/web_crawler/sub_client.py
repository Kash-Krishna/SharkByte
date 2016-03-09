import socket, sys, os, time
import crawler

HOST = "localhost"
PORT = 5000

""" Ping the server for list of all users
send back list to front end for display
"""
def look_for_sharks():
    skip

def get_shark_to_follow():
    shark_to_follow = raw_input("Please enter the username you wish to subscribe to: ")
    

"""
FIX: CHANGE PRINTS TO DISPLAYS ONTO UI
"""
if __name == "__main__":
    #server_socket
    global s_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_sock.settimeout(10)
    
    #connect to server
    try:
        s_socket.connect((HOST,PORT))
    except:
        print "Failure to connect to HOST at PORT: " + PORT
        sys.exit()

    #retrve user info from frontend
    shark = "Byte"
    
    
