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
    #print str(sys.argv)
    
    if argc <= 1:
        print "NOT ENOUGH ARGUMENTS"
        sys.exit()
    
    
