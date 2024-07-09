import socket
import json
import threading
import time

class PeerClient:
    def __init__(self, username, rendezvous_host, rendezvous_port):
        self.username = username
        self.rendezvous_host = rendezvous_host
        self.rendezvous_port = rendezvous_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        # print local address
        print(f"Local address: {self.sock.getsockname()}")
        self.peers = {}
        self.local_addr = self.sock.getsockname()

    def register_with_rendezvous(self):
        message = json.dumps({
            'type': 'register',
            'username': self.username,
            'local_addr': self.local_addr
        })
        self.sock.sendto(message.encode(), (self.rendezvous_host, self.rendezvous_port))

    def get_peer_list(self):
        message = json.dumps({
            'type': 'get_peers'
        })
        self.sock.sendto(message.encode(), (self.rendezvous_host, self.rendezvous_port))

    def update_peer_list(self):
        while True:
            self.get_peer_list()
            time.sleep(5)

    def send_message(self, message, broadcast=False):
        if broadcast:
            for peer, addr in self.peers.items():
                if peer != self.username:
                    print(f"Sending to {peer}: {message} ({addr['addr']})")
                    m = json.dumps({
                        'type': 'message',
                        'from': self.username,
                        'message': message
                    })
                    self.sock.sendto(m.encode(), tuple(addr['addr']))
        else:
            self.send_message(message, broadcast=True)

    def receive_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            try:
                response = json.loads(data.decode())
                if response['type'] == 'peer_list':
                    self.peers = response['peers']
                    print("Updated peer list:")
                    for peer, peer_info in self.peers.items():
                        print(f"  {peer}: {peer_info['addr']}")
                else:
                    print(f"Received from {addr}: {data.decode()}")
            except json.JSONDecodeError:
                print(f"Received from {addr}: {data.decode()}")

    def run(self):
        self.register_with_rendezvous()
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        update_thread = threading.Thread(target=self.update_peer_list)
        update_thread.start()

        print("You can start sending messages.")
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            self.send_message(message)

        print("Exiting...")

if __name__ == '__main__':
    username = input("Enter your username: ")
    client = PeerClient(username, '54.221.183.140', 5000)
    client.run()