#ifndef LOGGER_H
#define LOGGER_H

#include <ArduinoJson.h>
#include <FS.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>

class Logger {
public:
    Logger();
    void begin();
    void logEvent(const String& event, const String& details);
    String getLogs();
    QueueHandle_t logQueue;
private:
    DynamicJsonDocument logs;
    SemaphoreHandle_t mutex;
    TaskHandle_t taskHandle;
    static void task(void *pvParameters);
};

#endif