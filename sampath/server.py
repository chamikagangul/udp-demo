import socket
import os
from flask import Flask, send_file, Response
import threading
import random
import string
import io

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
FILE_DIR = "server_files"

app = Flask(__name__)

def start_rest_server():
    app.run(host='0.0.0.0', port=8000)

@app.route('/download/<filename>')
def download_file(filename):
    if filename == 'random':
        return send_random_file()
    return send_file(os.path.join(FILE_DIR, filename), as_attachment=True)

def send_random_file():
    content = generate_random_content(10 * 1024)  # 10KB of random text
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=random.txt"}
    )

def generate_random_content(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        filename = data.decode().strip()
        
        if filename == 'random':
            response = f"http://{UDP_IP}:8000/download/random"
            sock.sendto(response.encode(), addr)
        elif os.path.isfile(os.path.join(FILE_DIR, filename)):
            response = f"http://{UDP_IP}:8000/download/{filename}"
            sock.sendto(response.encode(), addr)
        else:
            sock.sendto(b"File not found", addr)

if __name__ == "__main__":
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    
    rest_thread = threading.Thread(target=start_rest_server)
    rest_thread.start()
    
    udp_server()