CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
SRC = $(wildcard src/*.cpp)
OBJ = $(SRC:.cpp=.o)
TARGET = temperature_monitor

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(TARGET) src/*.o
