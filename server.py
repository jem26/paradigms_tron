### Chris "Scary" Scaramella and Jamie Maher
## Paradigms Final Project
## Server Program

# This program will always be on on a raspberry pi.  It will wait for computers to make connections
# then facilitate a match between two computers.


from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

URL = "10.25.247.41"

class ConnectionGroup():
    def __init__(self):
        self.addr1 = None
        self.addr2 = None
        self.port = None
        self.command1 = None
        self.command2 = None
    def set_addr1(self,address):
        self.addr1 = address
    def set_addr2(self,address):
        self.addr2 = address


class TestConnection(Protocol):
    def connectionMade(self):
        print "New Connection Made\n"
        return
    def dataReceived(self,data):
        print data
        if data == "quit":
            reactor.stop()
            quit()
        else:
            self.transport.write(data)
        return
    def connectionLost(self, reason):
        print "Connection Lost"
        
class CommandConnection(Protocol):
    def __init__(self, group):
        self.group = group
    def connectionMade(self):
        if self.group.addr2 == None:
            # This is the first connection
            self.group.command1 = self
            self.addr = group.addr1
            self.transport.write("listen " + str(group.port))
        else:
            # This is the second connection
            self.group.command2 = self
            self.addr = group.addr2
            self.transport.write("connect " + str(group.port) + " " + group.addr1.host)
            self.group.set_addr1(None)
            self.group.set_addr2(None)
        return
    def dataReceived(self,data):
        print data
        return
    def connectionLost(self, reason):
        # Something happened
        self.group.set_addr1(None)
    	self.group.set_addr2(None)
        print "Something died, severing connections"
    def setGroup(self,group):
        self.group = group
        
class ServerConnectionFactory(ClientFactory):
    def __init__(self, connection_type, group):
        self.connection_type = connection_type
        self.command = CommandConnection(group)
        return
    def buildProtocol(self, addr):
        if self.connection_type == "command":
            if group.addr1 == None:
                group.set_addr1(addr)
            else:
                group.set_addr2(addr)
            self.command.setGroup(group)
            return self.command
    	return self.test_conn
    

if __name__== "__main__":
    group = ConnectionGroup()
    group.port = 41052
    reactor.listenTCP(40052, ServerConnectionFactory("command",group))
    print "Started listening for connection"

reactor.run()
