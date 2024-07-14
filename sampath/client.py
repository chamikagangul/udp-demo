import socket
import requests
import os
from tqdm import tqdm

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
DOWNLOAD_DIR = "client_downloads"

def request_file(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(filename.encode(), (UDP_IP, UDP_PORT))
    
    sock.settimeout(5)
    try:
        data, _ = sock.recvfrom(1024)
        response = data.decode()
        
        if response.startswith("http://"):
            print(f"File received: {filename}")
            download_file(response, filename)
        else:
            print(f"Server response: {response}")
    except socket.timeout:
        print("No response from server")
    finally:
        sock.close()

def download_file(url, filename):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    local_filename = os.path.join(DOWNLOAD_DIR, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        
        with open(local_filename, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in r.iter_content(chunk_size=1024):
                size = f.write(data)
                progress_bar.update(size)
    
    print(f"File downloaded and saved as: {local_filename}")

if __name__ == "__main__":
    while True:
        filename = input("Enter the filename to request (or 'quit' to exit): ")
        if filename.lower() == 'quit':
            break
        request_file(filename)