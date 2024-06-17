from twisted.internet import reactor, protocol
from twisted.internet.protocol import connectionDone
from twisted.python import failure 
class EchoClient(protocol.Protocol): 
    def connectionMade(self):
        msg = input("Enter the message to Server - ") 
        self.transport.write(msg.encode()) 

    def dataReceived(self, data):
        print ("Acknoledgement from Server -", data.decode()) 
        self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory): 
    def buildProtocol(self, addr): 
        return EchoClient()
        
reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run() 
