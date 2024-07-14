import socket
import json
import threading
import time
import random

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
                # write a response to a file 
                with open('punches.txt', 'a') as f:
                    f.write(f"{message['message']}\n and the address is {addr}\n")
    
    def bulk_port_scan(self,n_socks, range_start, range_end):
        sockets = []
        for _ in range(n_socks):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', 0))
            sockets.append(sock)

        for i, sock in enumerate(sockets):
            thread = threading.Thread(target=self.port_scan, args=(sock, i, range_start, range_end))
            thread.start()
            listen_thread = threading.Thread(target=self.receive_punch, args=(sock,))
            listen_thread.start()
            
            

    def port_scan(self, sock, i, range_start, range_end):
        message = json.dumps({
                'type': 'punch',
                'username': self.username,
                'message': f"punch {i}"
            })
        while True:
            port = random.randint(range_start, range_end)
            addr = (self.peer_ip, port)
            self.punch(sock, message, addr)
            time.sleep(0.01)
    
    def run(self):
        # self.port_scan(100, 6000, 7000)
        n_socks = input("Enter the number of ports to scan: ")
        self.bulk_port_scan(int(n_socks), 1, 65535)



        

if __name__ == '__main__':
    username = input("Enter your username: ")
    client = PeerClient(username, '4.213.171.161','3.82.57.239', 5000)
    client.run()