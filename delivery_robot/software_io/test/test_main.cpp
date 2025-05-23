// test/test_main.cpp
#include <unity.h>
#include <Arduino.h>
#include "line_follower.h"
#include "safe_controller.h"
#include "logger.h"

void setUp(void) {}
void tearDown(void) {}

void test_line_follower_calculate_error(void) {
    LineFollower follower;
    // Mock camera data (simplified)
    TEST_ASSERT_EQUAL(0, follower.calculateError()); // No line
}

void test_safe_controller_password(void) {
    Logger logger;
    SafeController safe(logger);
    safe.setPassword("1234");
    TEST_ASSERT_TRUE(safe.checkPassword("1234"));
    TEST_ASSERT_FALSE(safe.checkPassword("5678"));
}

void test_logger_event(void) {
    Logger logger;
    logger.begin();
    logger.logEvent("test_event", "Test details");
    String logs = logger.getLogs();
    TEST_ASSERT_TRUE(logs.indexOf("test_event") >= 0);
}

void setup() {
    delay(2000); // Wait for serial
    UNITY_BEGIN();
    RUN_TEST(test_line_follower_calculate_error);
    RUN_TEST(test_safe_controller_password);
    RUN_TEST(test_logger_event);
    UNITY_END();
}

void loop() {}