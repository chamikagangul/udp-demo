// rendezvous_server.js
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 8000; // You can change this port as needed

// Middleware
app.use(bodyParser.json());

// Store peer information
const peers = {};

// Register a peer
app.post('/register', (req, res) => {
    const { peer_id, address } = req.body;
    
    if (!peer_id || !address) {
        return res.status(400).json({ error: 'Missing peer_id or address' });
    }

    peers[peer_id] = address;
    res.json({ status: 'registered', peer_id });
});

// Get peer information
app.post('/get_peer', (req, res) => {
    const { requested_id, requester_id } = req.body;

    if (!requested_id || !requester_id) {
        return res.status(400).json({ error: 'Missing requested_id or requester_id' });
    }

    if (!(requested_id in peers)) {
        return res.status(404).json({ error: 'Requested peer not found' });
    }

    if (!(requester_id in peers)) {
        return res.status(404).json({ error: 'Requester not registered' });
    }

    res.json({
        status: 'success',
        peer_address: peers[requested_id],
        requester_address: peers[requester_id]
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Rendezvous server running on http://localhost:${port}`);
});