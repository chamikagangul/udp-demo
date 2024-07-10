import socket
import json
import threading
import time

class PeerClient:
    def __init__(self, username, peer_ip, rendezvous_ip, rendezvous_port):
        self.username = username
        self.peer_ip = peer_ip
        self.rendezvous_ip = rendezvous_ip
        self.rendezvous_port = rendezvous_port


        # sending a message to the rendezvous server to find a neerby port
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 0))
        sock.sendto(json.dumps({
            'type': 'register',
            'username': username,
            'message_sock': sock.getsockname()
        }).encode(), (rendezvous_ip, rendezvous_port))

    def punch(self,socket, message, addr):
        message = json.dumps({
            'type': 'punch',
            'username': self.username,
            'message': message
        })
        print(f"Sending punch to {addr}: {message}")
        socket.sendto(message.encode(), addr)
        
    def receive_punch(self, socket):
        while True:
            data, addr = socket.recvfrom(1024)
            message = json.loads(data.decode())
            if message['type'] == 'punch':
                print(f"Received punch from {addr}: {message['message']}")
    
    def bulk_port_scan(self,n_socks, range_start, range_end):
        sockets = []
        for _ in range(n_socks):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', 0))
            sockets.append(sock)

        for i, sock in enumerate(sockets):
            thread = threading.Thread(target=self.port_scan, args=(sock, i, range_start, range_end))
            thread.start()
            
            

    def port_scan(self, sock, i, range_start, range_end):
        message = json.dumps({
                'type': 'punch',
                'username': self.username,
                'message': f"punch {i}"
            })
        while True:
            for port in range(range_start, range_end):
                addr = (self.peer_ip, port)
                self.punch(sock, message, addr)
                time.sleep(0.1)
    
    def run(self):
        # self.port_scan(100, 6000, 7000)
        n_ports = input("Enter the number of ports to scan: ")
        range_start = input("Enter the start of the range: ")
        range_end = input("Enter the end of the range: ")
        self.bulk_port_scan(int(n_ports), int(range_start), int(range_end))



        

if __name__ == '__main__':
    username = input("Enter your username: ")
    client = PeerClient(username, '4.213.182.140','3.82.57.239', 5000)
    client.run()