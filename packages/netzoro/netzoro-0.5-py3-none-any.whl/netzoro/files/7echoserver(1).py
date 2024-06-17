from twisted.internet import protocol,reactor
from twisted.internet.protocol import connectionDone
from twisted.python import failure 

class echo(protocol.Protocol): 
    def dataReceived(self, data):
        print("Message from Client -", data.decode()) 
        print("Client Connected!")
        ack_msg = f"{data.decode()}"
        ack = "ACK[" + ack_msg + "]" 
        print("Acknoledgement Sent!") 
        self.transport.write(ack.encode()) 

    def connectionLost(self, reason):
        print("Client Disconnected")
        
class echofactory(protocol.Factory): 
    def buildProtocol(self, addr): 
        return echo() 
    
reactor.listenTCP(8000,echofactory())
reactor.run() 

