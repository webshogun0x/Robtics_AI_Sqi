#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// Wi-Fi Credentials
#define WIFI_SSID "your_ssid"
#define WIFI_PASSWORD "your_password"

// Laptop Server
#define SERVER_HOST "192.168.1.100" // Replace with laptop IP
#define SERVER_PORT 3000
#define WEBSOCKET_PATH "/"

// Motor Pins (L298N)
#define MOTOR_IN1 14
#define MOTOR_IN2 15
#define MOTOR_IN3 16
#define MOTOR_IN4 17

// Ultrasonic Sensor Pins
#define ULTRASONIC_TRIG 5
#define ULTRASONIC_ECHO 4
#define OBSTACLE_DISTANCE 30 // cm

// Servo Pin
#define SERVO_PIN 18

// Buzzer Pin
#define BUZZER_PIN 19

// Keypad Pins
#define KEYPAD_ROWS 4
#define KEYPAD_COLS 4
extern byte KEYPAD_ROW_PINS[KEYPAD_ROWS];
extern byte KEYPAD_COL_PINS[KEYPAD_COLS];

// Camera Settings
#define CAMERA_RESOLUTION FRAMESIZE_QVGA // 320x240
#define LINE_THRESHOLD 100 // Grayscale threshold

// Timing
#define DELIVERY_TIMEOUT 60000 // 60s
#define OBSTACLE_CHECK_INTERVAL 100 // ms
#define BUZZER_DURATION 1000 // ms

// Logger
#define MAX_LOGS 100

// FreeRTOS Settings
#define LINE_FOLLOWER_STACK_SIZE 4096
#define OBSTACLE_STACK_SIZE 2048
#define SAFE_STACK_SIZE 2048
#define NETWORK_STACK_SIZE 8192
#define LOGGER_STACK_SIZE 2048
#define LINE_FOLLOWER_PRIORITY 3
#define OBSTACLE_PRIORITY 3
#define SAFE_PRIORITY 2
#define NETWORK_PRIORITY 1
#define LOGGER_PRIORITY 1

#endif