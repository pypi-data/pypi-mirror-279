
from twisted.internet import protocol, reactor

class RARPClient(protocol.Protocol):
    def connectionMade(self):
        print('Connection made')
        self.sendNextMAC()

    def sendNextMAC(self):
        mac_address = input('Enter MAC address (or type "exit" to quit): ')
        self.transport.write(mac_address.encode())

    def dataReceived(self, data):
        response = data.decode().strip()
        print(response)
        if response.lower().startswith("exiting"):
            self.transport.loseConnection()
        else:
            self.sendNextMAC()

class RARPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RARPClient()

    def clientConnectionFailed(self, connector, reason):
        print(f'Connection failed: {reason.getErrorMessage()}')
        reactor.stop()

reactor.connectTCP('localhost', 8001, RARPClientFactory())
reactor.run()

