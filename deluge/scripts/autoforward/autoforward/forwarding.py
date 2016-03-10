import socket
import os
import sys

if __name__ == "__main__":
    ready = False
    HOST = ''
    PORT = 2000
    while(!ready):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket made")

        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print("Bind Failed: " + msg[0] + msg[1])
            sys.exit()

        print("Bind complete")

        
