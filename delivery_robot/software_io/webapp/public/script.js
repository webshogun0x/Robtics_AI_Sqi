const socket = io();
let isAuthenticated = false;

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const user = e.target.user.value;
    const pass = e.target.pass.value;
    if (user === 'admin' && pass === 'password123') {
        isAuthenticated = true;
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
    } else {
        alert('Invalid credentials');
    }
});

document.getElementById('deliveryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    if (!isAuthenticated) return alert('Please log in');
    const data = {
        destination: e.target.destination.value,
        password: e.target.password.value
    };
    fetch('/delivery', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `destination=${data.destination}&password=${data.password}`
    })
    .then(response => response.json())
    .then(data => alert(data.status));
});

function sendChat() {
    if (!isAuthenticated) return alert('Please log in');
    const msg = document.getElementById('chatInput').value;
    socket.emit('chat', msg);
    document.getElementById('chatInput').value = '';
}

socket.on('logs', (logs) => {
    document.getElementById('logs').textContent = JSON.stringify(logs, null, 2);
});

socket.on('chat', (messages) => {
    document.getElementById('chatMessages').innerHTML = messages.join('<br>');
});

socket.on('delivery', (data) => {
    document.getElementById('status').textContent = `Destination: ${data.destination}`;
});

setInterval(() => {
    fetch('/status')
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').textContent = JSON.stringify(data, null, 2);
    });
}, 2000);