#include "line_follower.h"
#include "config.h"

// support IDF 5.x
#ifndef portTICK_RATE_MS
#define portTICK_RATE_MS portTICK_PERIOD_MS
#endif

#include "esp_camera.h"

#define BOARD_WROVER_KIT 1

// WROVER-KIT PIN Map
#ifdef BOARD_WROVER_KIT

#define CAM_PIN_PWDN -1  //power down is not used
#define CAM_PIN_RESET -1 //software reset will be performed
#define CAM_PIN_XCLK 21
#define CAM_PIN_SIOD 26
#define CAM_PIN_SIOC 27

#define CAM_PIN_D7 35
#define CAM_PIN_D6 34
#define CAM_PIN_D5 39
#define CAM_PIN_D4 36
#define CAM_PIN_D3 19
#define CAM_PIN_D2 18
#define CAM_PIN_D1 5
#define CAM_PIN_D0 4
#define CAM_PIN_VSYNC 25
#define CAM_PIN_HREF 23
#define CAM_PIN_PCLK 22

#endif

// ESP32Cam (AiThinker) PIN Map
#ifdef BOARD_ESP32CAM_AITHINKER

#define CAM_PIN_PWDN 32
#define CAM_PIN_RESET -1 //software reset will be performed
#define CAM_PIN_XCLK 0
#define CAM_PIN_SIOD 26
#define CAM_PIN_SIOC 27

#define CAM_PIN_D7 35
#define CAM_PIN_D6 34
#define CAM_PIN_D5 39
#define CAM_PIN_D4 36
#define CAM_PIN_D3 21
#define CAM_PIN_D2 19
#define CAM_PIN_D1 18
#define CAM_PIN_D0 5
#define CAM_PIN_VSYNC 25
#define CAM_PIN_HREF 23
#define CAM_PIN_PCLK 22

#endif

LineFollower::LineFollower() : baseSpeed(150), taskHandle(NULL) {
    statusQueue = xQueueCreate(10, sizeof(String));
}

void LineFollower::begin() {
    pinMode(MOTOR_IN1, OUTPUT);
    pinMode(MOTOR_IN2, OUTPUT);
    pinMode(MOTOR_IN3, OUTPUT);
    pinMode(MOTOR_IN4, OUTPUT);
    stop();

    static camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = CAM_PIN_D0;
    config.pin_d3 = CAM_PIN_D3;
    config.pin_d4 = CAM_PIN_D4;
    config.pin_d1 = CAM_PIN_D1;
    config.pin_d2 = CAM_PIN_D2;
    config.pin_d5 = CAM_PIN_D5;
    config.pin_d6 = CAM_PIN_D6;
    config.pin_d7 = CAM_PIN_D7;
    config.pin_xclk = CAM_PIN_XCLK;
    config.pin_pclk = CAM_PIN_PCLK;
    config.pin_vsync = CAM_PIN_VSYNC;
    config.pin_href = CAM_PIN_HREF;
    config.pin_sccb_sda = CAM_PIN_SIOD;
    config.pin_sccb_scl = CAM_PIN_SIOC;
    config.pin_pwdn = CAM_PIN_PWDN;
    config.pin_reset = CAM_PIN_RESET;
    config.xclk_freq_hz = 20000000;
    config.frame_size = CAMERA_RESOLUTION;
    config.pixel_format = PIXFORMAT_GRAYSCALE;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.jpeg_quality = 12;
    config.fb_count = 1;

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed: 0x%x\n", err);
    }
}

void LineFollower::start() {
    xTaskCreatePinnedToCore(task, "LineFollower", LINE_FOLLOWER_STACK_SIZE, this, LINE_FOLLOWER_PRIORITY, &taskHandle, 1);
}

void LineFollower::stop() {
    analogWrite(MOTOR_IN1, 0);
    analogWrite(MOTOR_IN2, 0);
    analogWrite(MOTOR_IN3, 0);
    analogWrite(MOTOR_IN4, 0);
    String status = "{\"event\":\"stopped\"}";
    xQueueSend(statusQueue, &status, portMAX_DELAY);
}

void LineFollower::setSpeed(int speed) {
    baseSpeed = constrain(speed, 0, 255);
}

QueueHandle_t LineFollower::getStatusQueue() {
    return statusQueue;
}

void LineFollower::task(void *pvParameters) {
    LineFollower *self = (LineFollower *)pvParameters;
    while (true) {
        self->processImage();
        int error = self->calculateError();
        
        int leftSpeed = self->baseSpeed - error;
        int rightSpeed = self->baseSpeed + error;
        
        leftSpeed = constrain(leftSpeed, 0, 255);
        rightSpeed = constrain(rightSpeed, 0, 255);
        
        analogWrite(MOTOR_IN1, leftSpeed);
        analogWrite(MOTOR_IN2, 0);
        analogWrite(MOTOR_IN3, rightSpeed);
        analogWrite(MOTOR_IN4, 0);
        
        String status = "{\"event\":\"moving\"}";
        xQueueSend(self->statusQueue, &status, 0);
        
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void LineFollower::processImage() {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) return;

    for (int y = fb->height - 10; y < fb->height; y++) {
        for (int x = 0; x < fb->width; x++) {
            uint8_t pixel = fb->buf[y * fb->width + x];
            fb->buf[y * fb->width + x] = pixel < LINE_THRESHOLD ? 0 : 255;
        }
    }
    
    esp_camera_fb_return(fb);
}

int LineFollower::calculateError() {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) return 0;

    int center = fb->width / 2;
    int lineCenter = 0;
    int pixelCount = 0;

    for (int y = fb->height - 10; y < fb->height; y++) {
        for (int x = 0; x < fb->width; x++) {
            if (fb->buf[y * fb->width + x] == 0) {
                lineCenter += x;
                pixelCount++;
            }
        }
    }

    esp_camera_fb_return(fb);
    
    if (pixelCount == 0) return 0;
    lineCenter /= pixelCount;
    return (lineCenter - center) * 2;
}