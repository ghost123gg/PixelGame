import sys
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from _thread import *

class Client(ConnectionListener):
    def __init__(self, addr = "localhost", port = 25565):
        self.blockdata={}
        self.newdata=[]
        self.nicknamereceived=False
        self.Connect((addr, port))
        print("Client started")
        print("Ctrl-C to exit")
        # get a nickname from the user before starting
        print("request")
        connection.Send({"action": "nicknamerequest", "value":"1"})
        print("request")
        # launch our threaded input loop
        t = start_new_thread(self.InputLoop, ())

    def Loop(self):
        connection.Pump()
        self.Pump()

    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
            if len(self.newdata)!=0:
                print("newdata")
                connection.Send(self.newdata)
                self.newdata=""
            sleep(.01)

    #######################################
    ### Network event/message callbacks ###
    #######################################
    def Network_nicknamereceive(self, data):
        print("NicknameReceived")
        self.nicknamereceived=True
        connection.Send({"action": "levelrequest"})
    def Network_levelrecieve(self, data):
        pass
    def Network_placedblock(self, data):
        print("blockdata received")
        self.blockdata=data

    # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()
