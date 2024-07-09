import socket
import json

class RendezvousServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.peers = {}

    def run(self):
        print(f"Rendezvous server running on {self.host}:{self.port}")
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            
            if message['type'] == 'register':
                self.peers[message['username']] = {
                    'addr': addr,
                    'local_addr': message['local_addr']
                }
                print(f"Registered {message['username']} at {addr}")
            elif message['type'] == 'get_peers':
                response = json.dumps({
                    'type': 'peer_list',
                    'peers': self.peers
                })
                self.sock.sendto(response.encode(), addr)

if __name__ == '__main__':
    server = RendezvousServer('0.0.0.0', 5000)
    server.run()