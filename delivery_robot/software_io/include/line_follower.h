// include/line_follower.h
#ifndef LINE_FOLLOWER_H
#define LINE_FOLLOWER_H

#include <esp_camera.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <Arduino.h>
#include "config.h"


class LineFollower {
public:
    LineFollower();
    void begin();
    void start();
    void stop();
    void setSpeed(int speed);
    QueueHandle_t getStatusQueue();
private:
    int baseSpeed;
    TaskHandle_t taskHandle;
    QueueHandle_t statusQueue;
    static void task(void *pvParameters);
    void processImage();
    int calculateError();
};

#endif