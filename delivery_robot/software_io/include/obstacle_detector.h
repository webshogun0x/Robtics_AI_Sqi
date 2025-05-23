#ifndef OBSTACLE_DETECTOR_H
#define OBSTACLE_DETECTOR_H

#include <NewPing.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>

class LineFollower;
class Logger;

class ObstacleDetector {
public:
    ObstacleDetector(LineFollower& follower, Logger& logger);
    void begin();
    QueueHandle_t getStatusQueue();
private:
    LineFollower& follower;
    Logger& logger;
    TaskHandle_t taskHandle;
    QueueHandle_t statusQueue;
    static void task(void *pvParameters);
};

#endif