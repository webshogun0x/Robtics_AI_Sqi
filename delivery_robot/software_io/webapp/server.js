const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const bodyParser = require('body-parser');

const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server);

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

const logs = [];
const chatMessages = [];

app.post('/delivery', (req, res) => {
    const { destination, password } = req.body;
    io.emit('delivery', { destination, password });
    res.json({ status: 'delivery_set' });
});

app.get('/status', (req, res) => {
    res.json({ logs, chatMessages });
});

io.on('connection', (socket) => {
    console.log('Client connected');
    socket.emit('logs', logs);
    socket.emit('chat', chatMessages);
    
    socket.on('robot_connected', () => {
        console.log('Robot connected');
    });
    
    socket.on('log', (log) => {
        logs.push(log);
        io.emit('logs', logs);
    });
    
    socket.on('chat', (msg) => {
        chatMessages.push(msg);
        io.emit('chat', chatMessages);
    });
    
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

server.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});