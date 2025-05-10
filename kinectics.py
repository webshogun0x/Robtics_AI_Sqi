# kinematics.py
import numpy as np

class Kinematics:
    def __init__(self, config):
        self.config = config
        # Arm link lengths (meters, adjust for your arm)
        self.l1 = 0.1  # Base to shoulder
        self.l2 = 0.2  # Shoulder to elbow
        self.l3 = 0.2  # Elbow to wrist
        self.l4 = 0.1  # Wrist to gripper

    def inverse_kinematics(self, x, y, z):
        # Check workspace
        distance = np.sqrt(x**2 + y**2 + z**2)
        if distance > self.config.ARM_MAX_REACH:
            return None  # Outside workspace

        # Simplified inverse kinematics for 5-DOF arm
        # Base angle (theta1)
        theta1 = np.arctan2(y, x)

        # Adjust coordinates for shoulder-elbow-wrist plane
        x_prime = np.sqrt(x**2 + y**2)
        z_prime = z - self.l1

        # Elbow angle (theta3)
        D = (x_prime**2 + z_prime**2 - self.l2**2 - self.l3**2) / (2 * self.l2 * self.l3)
        if abs(D) > 1:
            return None  # Unreachable
        theta3 = np.arccos(D)

        # Shoulder angle (theta2)
        k1 = self.l2 + self.l3 * np.cos(theta3)
        k2 = self.l3 * np.sin(theta3)
        theta2 = np.arctan2(z_prime, x_prime) - np.arctan2(k2, k1)

        # Wrist pitch (theta4) to align gripper (simplified: keep gripper vertical)
        theta4 = -(theta2 + theta3)

        # Wrist roll (theta5, optional: keep at 0 for simplicity)
        theta5 = 0

        # Convert to degrees
        angles = [
            np.degrees(theta1),
            np.degrees(theta2),
            np.degrees(theta3),
            np.degrees(theta4),
            np.degrees(theta5)
        ]

        # Check angle limits
        for i, angle in enumerate(angles):
            if abs(angle) > self.config.SERVO_ANGLE_RANGE / 2:
                return None  # Angle out of range

        return angles