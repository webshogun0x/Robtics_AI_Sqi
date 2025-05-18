#include "../include/sensor_utils.hpp"
#include <fstream>
#include <string>

float readTemperature() {
    std::ifstream file("/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave"); // Replace with your sensor ID
    std::string line;
    if (file.is_open()) {
        std::getline(file, line);
        std::getline(file, line);
        size_t pos = line.find("t=");
        if (pos != std::string::npos) {
            std::string tempString = line.substr(pos + 2);
            return std::stof(tempString) / 1000;
        }
    }
    return -1;
}
