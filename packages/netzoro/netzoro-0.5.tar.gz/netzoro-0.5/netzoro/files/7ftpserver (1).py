from twisted.internet import reactor, protocol 
import os

from twisted.internet.protocol import connectionDone
from twisted.python import failure

class FileTransferProtocol(protocol.Protocol): 
    def connectionMade(self): 
        print("Client connected.") 

    def dataReceived(self, data): 
        if data == b"SEND": 
            self.transport.write(b"READY") 
            self.transferFile = True 
        elif self.transferFile: 
            with open("received_file.txt", "wb") as f: 
                f.write(data) 
            self.transport.write(b"RECEIVED") 
            self.transferFile = False
        else: 
            self.transport.write(b"ERROR")
    
    def connectionLost(self, reason):
        print("Client Disconnected")
            

class FileTransferFactory(protocol.Factory): 
    protocol = FileTransferProtocol 

    
if __name__ == "__main__": 
    reactor.listenTCP(7000, FileTransferFactory()) 
    print("Server started.")
    reactor.run() 
