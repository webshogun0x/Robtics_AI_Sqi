#include "../include/servo_control.hpp"
#include <wiringPi.h>
#include <softPwm.h>

int servoPin;

void initServo(int pin) {
    wiringPiSetupGpio(); // BCM pin numbering
    servoPin = pin;
    softPwmCreate(servoPin, 0, 200); // Range for PWM
}

void setServoAngle(int angle) {
    int pulse = (angle * 11) / 10 + 50; // Convert to servo pulse width
    softPwmWrite(servoPin, pulse);
}
