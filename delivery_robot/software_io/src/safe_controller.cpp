// src/safe_controller.cpp
#include "safe_controller.h"
#include "logger.h"
#include "config.h"

Servo servo;

void intial_PWM_setup() {
    	// Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	servo.setPeriodHertz(50);    // standard 50 hz servo
	servo.attach(SERVO_PIN, 1000, 2000); // attaches the servo on pin 18 to the servo object
	// using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep
}

SafeController::SafeController(Logger& l) : keypad(makeKeymap(keypadMap), KEYPAD_ROW_PINS, KEYPAD_COL_PINS, KEYPAD_ROWS, KEYPAD_COLS), logger(l) {
    password = "1234";
    statusQueue = xQueueCreate(10, sizeof(String));
}

void SafeController::begin() {
    servo.attach(SERVO_PIN);
    lock();
    xTaskCreatePinnedToCore(task, "SafeController", SAFE_STACK_SIZE, this, SAFE_PRIORITY, &taskHandle, 0);
}

void SafeController::setPassword(const String& pwd) {
    password = pwd;
}

QueueHandle_t SafeController::getStatusQueue() {
    return statusQueue;
}

void SafeController::task(void *pvParameters) {
    SafeController *self = (SafeController *)pvParameters;
    String input = "";
    bool isStopped = false;
    
    while (true) {
        char key = self->keypad.getKey();
        if (key) {
            input += key;
            if (input.length() >= 4) {
                if (self->checkPassword(input)) {
                    self->unlock();
                    String status = "{\"event\":\"delivery_success\"}";
                    xQueueSend(self->statusQueue, &status, portMAX_DELAY);
                    self->logger.logEvent("delivery_success", "Safe unlocked");
                } else {
                    String status = "{\"event\":\"wrong_password\",\"details\":\"" + input + "\"}";
                    xQueueSend(self->statusQueue, &status, portMAX_DELAY);
                    self->logger.logEvent("wrong_password", "Attempt: " + input);
                    if (isStopped) {
                        self->logger.logEvent("tampering", "Wrong password during stop: " + input);
                    }
                }
                input = "";
            }
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

bool SafeController::checkPassword(const String& input) {
    return input == password;
}

void SafeController::unlock() {
    servo.write(90);
}

void SafeController::lock() {
    servo.write(0);
}