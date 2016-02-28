import socket, sys, os, time
import cPickle as pickle
from shark import Shark #sharks are users

HOST = 'localhost'
PORT = ''

def clearScreen():
    os.system('clear')
    return

if __name__ == "__main__":
    argc = len(sys.argv)
    
    if argc <= 1:
        print "NOT ENOUGH ARGUMENTS"
        sys.exit()

    source = sys.argv[1]
    query = sys.argv[2]
    #if source is "kat.cr" or source is "kat":
        
