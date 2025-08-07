#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESPmDNS.h>

// WiFi credentials
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// Pin to control the lock
const int lockPin = 5; // Use any GPIO you wired to relay/lock
bool isUnlocked = false;

// Unlock duration (milliseconds)
const unsigned long unlockDuration = 5000;
unsigned long unlockTime = 0;

// Async web server on port 80
AsyncWebServer server(80);

void setupWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP: ");
  Serial.println(WiFi.localIP());
}

void setupMDNS() {
  if (!MDNS.begin("esp32")) {
    Serial.println("Error setting up MDNS responder!");
  } else {
    Serial.println("mDNS responder started: http://esp32.local");
  }
}

void setupServer() {
  // /unlock endpoint
  server.on("/unlock", HTTP_GET, [](AsyncWebServerRequest *request){
    if (!isUnlocked) {
      digitalWrite(lockPin, HIGH);  // Activate relay/solenoid
      unlockTime = millis();
      isUnlocked = true;
      Serial.println("Shelf unlocked.");
    }
    request->send(200, "text/plain", "Shelf unlocked");
  });

  // /status endpoint
  server.on("/status", HTTP_GET, [](AsyncWebServerRequest *request){
    String status = isUnlocked ? "UNLOCKED" : "LOCKED";
    request->send(200, "application/json", "{\"status\": \"" + status + "\"}");
  });

  // Start server
  server.begin();
  Serial.println("HTTP server started.");
}

void setup() {
  Serial.begin(115200);
  pinMode(lockPin, OUTPUT);
  digitalWrite(lockPin, LOW);  // Default locked

  setupWiFi();
  setupMDNS();
  setupServer();
}

void loop() {
  // Auto-lock after timeout
  if (isUnlocked && (millis() - unlockTime > unlockDuration)) {
    digitalWrite(lockPin, LOW); // Lock again
    isUnlocked = false;
    Serial.println("Shelf auto-locked.");
  }
}
