#include "network.h"
#include "line_follower.h"
#include "safe_controller.h"
#include "logger.h"
#include "config.h"

Network::Network(LineFollower& f, SafeController& s, Logger& l)
    : follower(f), safe(s), logger(l), taskHandle(NULL) {
    deliveryQueue = xQueueCreate(5, sizeof(String));
    chatQueue = xQueueCreate(10, sizeof(String));
}

void Network::begin() {
    xTaskCreatePinnedToCore(task, "Network", NETWORK_STACK_SIZE, this, NETWORK_PRIORITY, &taskHandle, 0);
}

QueueHandle_t Network::getDeliveryQueue() {
    return deliveryQueue;
}

void Network::task(void *pvParameters) {
    Network *self = (Network *)pvParameters;
    
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        vTaskDelay(pdMS_TO_TICKS(500));
        Serial.print(".");
    }
    Serial.println(WiFi.localIP());
    
    self->webSocket.begin(SERVER_HOST, SERVER_PORT, WEBSOCKET_PATH);
    self->webSocket.onEvent([self](WStype_t type, uint8_t *payload, size_t length) {
        self->webSocketEvent(type, payload, length);
    });
    self->webSocket.setReconnectInterval(5000);
    
    while (true) {
        self->webSocket.loop();
        
        String chatMsg;
        if (xQueueReceive(self->chatQueue, &chatMsg, 0)) {
            self->webSocket.sendTXT(chatMsg);
        }
        
        self->sendStatus();
        
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void Network::webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {
    switch (type) {
        case WStype_DISCONNECTED:
            Serial.println("WebSocket Disconnected");
            break;
        case WStype_CONNECTED:
            Serial.println("WebSocket Connected");
            webSocket.sendTXT("{\"type\":\"robot_connected\"}");
            break;
        case WStype_TEXT:
            String message = String((char *)payload);
            StaticJsonDocument<200> doc;
            deserializeJson(doc, message);
            String type = doc["type"];
            if (type == "chat") {
                String msg = doc["message"];
                xQueueSend(chatQueue, &msg, portMAX_DELAY);
            }
            break;
    }
}

void Network::sendStatus() {
    StaticJsonDocument<512> doc;
    String followerStatus, safeStatus, obstacleStatus, logEntry;
    
    if (xQueueReceive(follower.getStatusQueue(), &followerStatus, 0)) {
        doc["follower"] = followerStatus;
    }
    if (xQueueReceive(safe.getStatusQueue(), &safeStatus, 0)) {
        doc["safe"] = safeStatus;
    }
    if (xQueueReceive(logger.logQueue, &logEntry, 0)) {
        doc["log"] = logEntry;
        webSocket.sendTXT(logEntry);
    }
    
    String output;
    serializeJson(doc, output);
    webSocket.sendTXT(output);
}