from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class ChatClient(DatagramProtocol):
    def startProtocol(self):
        host = "127.0.0.1"  # Change this to the IP address of your server
        port = 5000  # Make sure this matches the port your server is listening on
        username = input("Enter your username: ")

        # Send the username to the server
        self.transport.write(username.encode('utf-8'), (host, port))

        # Start sending messages
        reactor.callInThread(self.send_messages)

    def send_messages(self):
        while True:
            message = input("Enter your message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                reactor.stop()
                break
            self.transport.write(message.encode('utf-8'), ("127.0.0.1", 5000))

    def datagramReceived(self, data, addr):
        print(data.decode('utf-8'))

if __name__ == "__main__":
    reactor.listenUDP(0, ChatClient())
    reactor.run()
