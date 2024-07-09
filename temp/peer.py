# peer.py
import requests
import socket
import threading
import time
import json

RENDEZVOUS_SERVER_URL = 'http://localhost:6000'

def peer(peer_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 0))
    my_addr = sock.getsockname()
    my_addr = get_my_ip(), my_addr[1]
    print(f"My address: {my_addr}")

    # Register with rendezvous server
    response = requests.post(f'{RENDEZVOUS_SERVER_URL}/register', 
                             json={'peer_id': peer_id, 'address': my_addr},
                             verify=True)  # Set verify=False if using self-signed cert
    print(response.json())

    # Get peer info
    other_id = input("Enter peer ID to connect to: ")
    response = requests.post(f'{RENDEZVOUS_SERVER_URL}/get_peer', 
                             json={'requested_id': other_id, 'requester_id': peer_id},
                             verify=True)  # Set verify=False if using self-signed cert
    data = response.json()
    print(data)
    if data['status'] == 'success':
        peer_addr = tuple(data['peer_address'])
        print(f"Peer address: {peer_addr}")

        # Start hole punching
        punch_thread = threading.Thread(target=hole_punch, args=(sock, peer_addr))
        punch_thread.start()

        # Start message handling
        msg_thread = threading.Thread(target=handle_messages, args=(sock,))
        msg_thread.start()

        # Send messages
        while True:
            msg = input("Enter message: ")
            sock.sendto(msg.encode(), peer_addr)
    else:
        print("Peer not found")

def hole_punch(sock, peer_addr):
    while True:
        sock.sendto(b"punch", peer_addr)
        time.sleep(1)

def handle_messages(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        if data != b"punch":
            print(f"Received from {addr}: {data.decode()}")

# get my ip address
def get_my_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

if __name__ == "__main__":
    my_id = input("Enter your peer ID: ")
    peer(my_id)