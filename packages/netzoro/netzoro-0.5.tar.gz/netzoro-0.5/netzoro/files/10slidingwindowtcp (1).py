from twisted.internet import protocol, reactor


class SelectiveRepeatProtocol(protocol.Protocol):
    def __init__(self):
        self.window_size = 4  # Size of the sender and receiver window
        self.send_base = 0  # Sequence number of the oldest unacknowledged packet
        self.send_next = 0  # Sequence number of the next packet to be sent
        self.recv_base = 0  # Sequence number of the oldest unprocessed packet

        self.buffer = ['Packet0', 'Packet1', 'Packet2', 'Packet3'] 

    def connectionMade(self):
        print("Connection established.")
        self.sendPackets()

    def dataReceived(self, data):
        # Simulate packet loss
        if data != b"ACK":
            print("Packet lost!")
            return

        print("ACK received.")
        self.send_base += 1
        self.send_next += 1
        self.sendPackets()

    def sendPackets(self):
        while self.send_next < self.send_base + self.window_size and self.send_next < len(self.buffer):
            packet = self.buffer[self.send_next]
            print("Sending packet:", packet)
            self.transport.write(packet.encode())
            self.send_next += 1

    def connectionLost(self, reason):
        print("Connection lost.")


class SelectiveRepeatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SelectiveRepeatProtocol()

reactor.listenTCP(8000, SelectiveRepeatFactory())
reactor.run()
