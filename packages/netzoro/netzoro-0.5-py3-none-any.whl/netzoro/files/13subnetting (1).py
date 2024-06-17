from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineOnlyReceiver
import ipaddress

SUBNET = ipaddress.IPv4Network("192.168.0.0/24")

class SubnetCheckerProtocol(LineOnlyReceiver):
    def connectionMade(self):
        self.sendLine(b"Enter an IP address to check:")

    def lineReceived(self, line):
        ip_address = line.strip().decode()
        result = b"IP address is within the subnet" if self.is_in_subnet(ip_address) else b"IP address is outside the subnet"
        self.sendLine(result)
        self.transport.loseConnection()

    def is_in_subnet(self, ip_address):
        try:
            return ipaddress.IPv4Address(ip_address) in SUBNET
        except ipaddress.AddressValueError:
            return False

if __name__ == "__main__":
    reactor.listenTCP(8000, protocol.Factory.forProtocol(SubnetCheckerProtocol))
    print("Subnet checker server is running...")
    reactor.run()
