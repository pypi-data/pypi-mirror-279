from twisted.internet import protocol, reactor

class RARPServer(protocol.Protocol):
    def connectionMade(self):
        print('Connection made')
        self.transport.write(b"Enter MAC address (or 'exit' to quit): ")

    def dataReceived(self, data):
        mac_address = data.decode().strip()
        if mac_address.lower() == 'exit':
            print('Exiting...')
            self.transport.loseConnection()
            return

        response = f"IP FOR MAC {mac_address} is 192.168.1.1"
        self.transport.write(response.encode())
        self.transport.write(b"Enter 'exit' to quit): ")

class RARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RARPServer()

reactor.listenTCP(8001, RARPServerFactory())
reactor.run()
