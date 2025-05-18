CXX = g++
CXXFLAGS = -std=c++17 -Wall -lwiringPi -Iinclude
SRC = $(wildcard src/*.cpp)
TARGET = servo_control

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(TARGET) src/*.o
