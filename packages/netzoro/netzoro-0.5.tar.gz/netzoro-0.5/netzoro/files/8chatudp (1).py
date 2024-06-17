from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class ChatServer(DatagramProtocol):
    def __init__(self):
        self.users = {}  # maps user addresses to usernames

    def datagramReceived(self, data, addr):
        message = data.decode('utf-8').strip()

        # Check if the message starts with a known command
        if message.startswith("/username "):
            # Extract the username from the command
            username = message.split()[1]
            self.users[addr] = username
            self.transport.write(f"Username set to {username}\n".encode('utf-8'), addr)
        else:
            # Normal chat message
            username = self.users.get(addr, "Unknown")
            broadcast_message = f"<{username}> {message}\n"
            addresses_to_send = [(host, port) for (host, port) in self.users if (host, port) != addr]
            self.transport.write(broadcast_message.encode('utf-8'), addresses_to_send)

if __name__ == "__main__":
    reactor.listenUDP(5000, ChatServer())
    print("Server started.")
    reactor.run()

