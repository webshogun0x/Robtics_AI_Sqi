# Set Up Web App on Laptop
## Install Node.js: nodejs.org.

Install Dependencies:
```bash

cd webapp
npm install express socket.io body-parser
```
Run Server:
```bash

node server.js
```
## Configure ESP32-S3:
Update SERVER_HOST in include/config.h with your laptop’s IP (e.g., 192.168.1.100).

# Step 4: Build and Upload
## Build:
In PlatformIO, click Build (or pio run).

## Upload Firmware:
* Connect ESP32-S3 via USB.
* Click Upload (or pio run -t upload).
* Upload SPIFFS:
* Click Upload Filesystem Image (or pio run -t uploadfs) to upload data/.

* Monitor: Use Serial Monitor (pio device monitor) to view IP address and logs.

# Run Tests
## Unit Tests:
* Run pio test to execute test/test_main.cpp.

* Check Serial Monitor for results.

## Integration Tests:
* Add -DTEST_MODE to build_flags in platformio.ini.
* Upload and monitor Serial output.

# Test System
* Open http://<laptop_ip>:3000 in a browser.

* Log in (admin/password123).

* Set delivery destination/password.

* Monitor navigation, obstacle stops, keypad input, chat, and logs via WebSocket.

* Verify logs in SPIFFS (data/logs.json) and web app.

* Set Up Web App on Laptop
* Install Node.js: nodejs.org.
