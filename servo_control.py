# servo_control.py
from adafruit_pca9685 import PCA9685
import board
import busio
import time

class ServoControl:
    def __init__(self, config):
        self.config = config
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50  # Hz for servos

    def set_angle(self, channel, angle):
        # Map angle (0-180) to PWM pulse (500-2500 µs)
        pulse = (angle / self.config.SERVO_ANGLE_RANGE) * (self.config.SERVO_MAX_PULSE - self.config.SERVO_MIN_PULSE) + self.config.SERVO_MIN_PULSE
        duty = int(pulse * self.pca.frequency / 1000000 * 65535)
        self.pca.channels[channel].duty_cycle = duty

    def open_gripper(self):
        self.set_angle(self.config.SERVO_CHANNELS[5], self.config.GRIPPER_OPEN_ANGLE)

    def close_gripper(self):
        self.set_angle(self.config.SERVO_CHANNELS[5], self.config.GRIPPER_CLOSED_ANGLE)

    def set_arm_angles(self, angles):
        if angles is None:
            return False
        for i, angle in enumerate(angles):
            self.set_angle(self.config.SERVO_CHANNELS[i], angle + 90)  # Center at 90°
        return True