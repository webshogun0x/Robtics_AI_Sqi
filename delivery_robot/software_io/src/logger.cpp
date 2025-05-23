#include "logger.h"
#include "config.h"
#include <SPIFFS.h>

Logger::Logger() : logs(MAX_LOGS * 100) {
    mutex = xSemaphoreCreateMutex();
    logQueue = xQueueCreate(20, sizeof(String));
}

void Logger::begin() {
    if (!SPIFFS.begin(true)) {
        Serial.println("SPIFFS Mount Failed");
        return;
    }
    File file = SPIFFS.open("/logs.json", "r");
    if (file) {
        deserializeJson(logs, file);
        file.close();
    }
    xTaskCreatePinnedToCore(task, "Logger", LOGGER_STACK_SIZE, this, LOGGER_PRIORITY, &taskHandle, 0);
}

void Logger::logEvent(const String& event, const String& details) {
    String logEntry = "{\"event\":\"" + event + "\",\"details\":\"" + details + "\",\"time\":\"" + String(millis()) + "\"}";
    xQueueSend(logQueue, &logEntry, portMAX_DELAY);
}

String Logger::getLogs() {
    xSemaphoreTake(mutex, portMAX_DELAY);
    String output;
    serializeJson(logs, output);
    xSemaphoreGive(mutex);
    return output;
}

void Logger::task(void *pvParameters) {
    Logger *self = (Logger *)pvParameters;
    String logEntry;
    
    while (true) {
        if (xQueueReceive(self->logQueue, &logEntry, portMAX_DELAY)) {
            xSemaphoreTake(self->mutex, portMAX_DELAY);
            JsonObject entry = self->logs.createNestedObject();
            entry["time"] = String(millis());
            entry["event"] = logEntry.substring(logEntry.indexOf("\"event\":\"") + 9, logEntry.indexOf("\",\"details\""));
            entry["details"] = logEntry.substring(logEntry.indexOf("\"details\":\"") + 11, logEntry.lastIndexOf("\""));
            
            File file = SPIFFS.open("/logs.json", "w");
            serializeJson(self->logs, file);
            file.close();
            
            xSemaphoreGive(self->mutex);
            
            // Send to WebSocket (handled by Network task)
        }
    }
}