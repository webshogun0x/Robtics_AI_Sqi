#include "obstacle_detector.h"
#include "line_follower.h"
#include "logger.h"
#include "config.h"

ObstacleDetector::ObstacleDetector(LineFollower& f, Logger& l) : follower(f), logger(l), taskHandle(NULL) {
    statusQueue = xQueueCreate(10, sizeof(String));
}

void ObstacleDetector::begin() {
    xTaskCreatePinnedToCore(task, "ObstacleDetector", OBSTACLE_STACK_SIZE, this, OBSTACLE_PRIORITY, &taskHandle, 1);
}

QueueHandle_t ObstacleDetector::getStatusQueue() {
    return statusQueue;
}

void ObstacleDetector::task(void *pvParameters) {
    ObstacleDetector *self = (ObstacleDetector *)pvParameters;
    NewPing sonar(ULTRASONIC_TRIG, ULTRASONIC_ECHO, 400);
    
    while (true) {
        int distance = sonar.ping_cm();
        if (distance > 0 && distance < OBSTACLE_DISTANCE) {
            self->follower.stop();
            String status = "{\"event\":\"obstacle_detected\"}";
            xQueueSend(self->statusQueue, &status, portMAX_DELAY);
            self->logger.logEvent("obstacle_detected", "Distance: " + String(distance) + "cm");
            
            while (sonar.ping_cm() < OBSTACLE_DISTANCE && sonar.ping_cm() > 0) {
                vTaskDelay(pdMS_TO_TICKS(OBSTACLE_CHECK_INTERVAL));
            }
            
            status = "{\"event\":\"obstacle_cleared\"}";
            xQueueSend(self->statusQueue, &status, portMAX_DELAY);
            self->logger.logEvent("obstacle_cleared", "Resuming navigation");
        }
        vTaskDelay(pdMS_TO_TICKS(OBSTACLE_CHECK_INTERVAL));
    }
}