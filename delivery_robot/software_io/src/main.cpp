// src/main.cpp
#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiUdp.h>
#include "config.h"
#include "line_follower.h"
#include "obstacle_detector.h"
#include "safe_controller.h"
#include "logger.h"
#include "network.h"

LineFollower follower;
Logger logger;
SafeController safe(logger);
ObstacleDetector detector(follower, logger);
Network network(follower, safe, logger);

unsigned long deliveryStartTime = 0;
bool isDelivering = false;

void setup() {
    Serial.begin(115200);
    logger.begin();
    follower.begin();
    detector.begin();
    safe.begin();
    network.begin();
    
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);
}

void loop() {
    if (isDelivering && millis() - deliveryStartTime > DELIVERY_TIMEOUT) {
        follower.stop();
        digitalWrite(BUZZER_PIN, HIGH);
        vTaskDelay(pdMS_TO_TICKS(BUZZER_DURATION));
        digitalWrite(BUZZER_PIN, LOW);
        logger.logEvent("delivery_timeout", "Timeout reached");
        isDelivering = false;
    }
    
    String delivery;
    if (xQueueReceive(network.getDeliveryQueue(), &delivery, 0)) {
        StaticJsonDocument<200> doc;
        deserializeJson(doc, delivery);
        String dest = doc["destination"];
        String pwd = doc["password"];
        safe.setPassword(pwd);
        follower.setSpeed(150);
        isDelivering = true;
        deliveryStartTime = millis();
        logger.logEvent("delivery_started", "Destination: " + dest);
    }
    
    vTaskDelay(pdMS_TO_TICKS(10));
}