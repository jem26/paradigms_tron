### Chris "Scary" Scaramella and Jamie Maher
## Paradigms Final Project
## Client Program

# This program will run on the computer playing the game
# It will connect to the raspberry pi


from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

URL = "10.25.247.41"

class ConnectionGroup():
    def __init__(self):
        self.command = None
    	self.data = None

class TestConnection(Protocol):
    def __init__(self):
        self.address = "Unknown"
        self.player = 0
        return
    def connectionMade(self):
        print "New Connection Made\n"
        return
    def dataReceived(self,data):
        print data
        if data == "quit":
            reactor.stop()
            quit()
        return
    def connectionLost(self, reason):
        print "Connection Lost\n"
        return
    def addAddress(self, address):
        self.address = address
        return

class CommandConnection(Protocol):
    def __init__(self,group):
        self.player = 0
        self.group = group
    def connectionMade(self):
        print "Command Connection Established"
        self.group.command = self
    def dataReceived(self,data):
        print "Command: " + data
        info = data.split(" ")
        if info[0] == "listen":
            self.player = 1
            reactor.listenTCP(int(info[1]), ClientConnectionFactory("data", self.group))
        elif info[0] == "connect":
            self.player = 2
            reactor.connectTCP(info[2], int(info[1]), ClientConnectionFactory("data", self.group))
        self.transport.write("Player " + str(self.player) + " reporting in!")
    def connectionLost(self, reason):
        print "Command Connection Lost"



class DataConnection(Protocol):
    def __init__(self,group):
        self.group = group
    def connectionMade(self):
        self.group.data = self
        self.group.command.group = self.group
        self.player = self.group.command.player
        print "Data Connection Established"
        print "I am player " + str(self.player)
    def dataReceived(self,data):
        print data
    def connectionLost(self, reason):
        print "Connection Lost"
        
class ClientConnectionFactory(ClientFactory):
    def __init__(self, connection_type, group):
        self.connection_type = connection_type
        self.test_conn = TestConnection()
        self.command = CommandConnection(group)
        self.data = DataConnection(group)
        return
    def buildProtocol(self,addr):
        if self.connection_type == "command":
            return self.command
        elif self.connection_type == "data":
            return self.data
        else:
            return self.test_conn

if __name__ == "__main__":
    group = ConnectionGroup()
    reactor.connectTCP(URL, 40000, ClientConnectionFactory("command",group))
    print "Started listening for connection\n"

reactor.run()
            
