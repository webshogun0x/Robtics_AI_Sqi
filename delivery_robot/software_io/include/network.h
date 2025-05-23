#ifndef NETWORK_H
#define NETWORK_H

#include <WiFi.h>
#include <HTTPClient.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>

class LineFollower;
class SafeController;
class Logger;

class Network {
public:
    Network(LineFollower& follower, SafeController& safe, Logger& logger);
    void begin();
    QueueHandle_t getDeliveryQueue();
private:
    LineFollower& follower;
    SafeController& safe;
    Logger& logger;
    WebSocketsClient webSocket;
    TaskHandle_t taskHandle;
    QueueHandle_t deliveryQueue;
    QueueHandle_t chatQueue;
    static void task(void *pvParameters);
    void webSocketEvent(WStype_t type, uint8_t *payload, size_t length);
    void sendStatus();
};

#endif