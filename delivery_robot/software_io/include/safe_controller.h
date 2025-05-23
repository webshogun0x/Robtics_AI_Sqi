#ifndef SAFE_CONTROLLER_H
#define SAFE_CONTROLLER_H
#include <ESP32Servo.h>
#include <Keypad.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <Arduino.h>
#include "config.h"

class Logger;

extern Servo servo;

class SafeController {
public:
    SafeController(Logger& logger);
    void begin();
    void setPassword(const String& pwd);
    QueueHandle_t getStatusQueue();

private:
    Logger& logger;
    String password;
    char keypadMap[KEYPAD_ROWS][KEYPAD_COLS] = {
        {'1', '2', '3', 'A'},
        {'4', '5', '6', 'B'},
        {'7', '8', '9', 'C'},
        {'*', '0', '#', 'D'}
    };
    Keypad keypad;
    TaskHandle_t taskHandle;
    QueueHandle_t statusQueue;
    static void task(void *pvParameters);
    bool checkPassword(const String& input);
    void unlock();
    void lock();
};

#endif