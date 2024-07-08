# rendezvous_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import ssl

app = Flask(__name__)
CORS(app)

peers = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    peer_id = data['peer_id']
    address = data['address']
    peers[peer_id] = address
    return jsonify({"status": "registered", "peer_id": peer_id})

@app.route('/get_peer', methods=['POST'])
def get_peer():
    data = request.json
    requested_id = data['requested_id']
    requester_id = data['requester_id']
    if requested_id in peers:
        return jsonify({
            "status": "success",
            "peer_address": peers[requested_id],
            "requester_address": peers[requester_id]
        })
    else:
        return jsonify({"status": "not_found"})
    
@app.route('/', methods=['GET'])
def get_peers():
    print(peers)
    return jsonify(peers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)