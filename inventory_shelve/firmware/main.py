import network
import usocket as socket
import machine
import time

# Wi-Fi credentials
SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'

# Lock pin
lock_pin = machine.Pin(5, machine.Pin.OUT)
lock_pin.off()  # Lock closed

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print('Connected to Wi-Fi:', wlan.ifconfig())

# Simple HTTP server
def handle_request(client):
    request = client.recv(1024).decode()
    if 'GET /unlock' in request:
        lock_pin.on()  # Unlock
        time.sleep(30)  # Open for 30 seconds
        lock_pin.off()  # Lock
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nShelf unlocked'
    else:
        response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot found'
    client.send(response.encode())
    client.close()

# Start server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)
print('Server running on', wlan.ifconfig()[0])

while True:
    client, _ = s.accept()
    handle_request(client)