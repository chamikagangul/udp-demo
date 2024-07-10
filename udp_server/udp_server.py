import socket
import json

class RendezvousServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock2.bind((self.host, 6000))
        self.peers = {}

    def run(self):
        print(f"Rendezvous server running on {self.host}:{self.port}")
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            print(f"Received message from {addr}: {message}")
            
            if message['type'] == 'register':
                message_addr = addr[0]
                message_port = message['message_sock'][1]
                
                self.peers[message['username']] = {
                    'addr': addr,
                    'message_addr': [message_addr, message_port],
                }
                print(f"Registered {message['username']} at {addr}")
            elif message['type'] == 'get_peers':
                print(f"Sending peer list to {addr}")
                response = json.dumps({
                    'type': 'peer_list',
                    'peers': self.peers
                })
                self.sock.sendto(response.encode(), addr)
                self.sock2.sendto("test ping".encode(), addr)

if __name__ == '__main__':
    server = RendezvousServer('0.0.0.0', 5000)
    server.run()