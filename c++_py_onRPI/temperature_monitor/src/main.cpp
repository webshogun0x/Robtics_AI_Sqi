#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include "../include/sensor_utils.hpp"

int main() {
    while (true) {
        float tempC = readTemperature();
        std::cout << "Current Temperature: " << tempC << "°C" << std::endl;
        sleep(2);
    }
    return 0;
}
