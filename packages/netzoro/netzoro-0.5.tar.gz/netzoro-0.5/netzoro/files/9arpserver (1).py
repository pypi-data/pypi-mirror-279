from twisted.internet import protocol,reactor
table = {}
table["192.168.1.1"] = "00:11:22:33:44:55"

class dns_server(protocol.Protocol):
    def connectionMade(self):
        print('connection made')
    
    def dataReceived(self, data: bytes):
        global table
        a = data.decode()
        ip = table.get(a)
        if ip is not None:
            response = f"MAC FOR {a} is {ip}"
        else:
            response = f"NO IP FOR DOMAIN {a}"
        self.transport.write(response.encode())

class dns_factory(protocol.Factory):
    def buildProtocol(self, addr):
        return dns_server()

reactor.listenTCP(8000, dns_factory())
reactor.run()