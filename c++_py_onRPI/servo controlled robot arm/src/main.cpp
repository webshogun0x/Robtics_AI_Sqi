#include <iostream>
#include <unistd.h>
#include "../include/servo_control.hpp"

int main() {
    initServo(18); // GPIO pin 18 (PWM)
    for (int angle = 0; angle <= 180; angle += 10) {
        setServoAngle(angle);
        sleep(1);
    }
    return 0;
}
