# tracker.py
import time
import numpy as np
from camera import Camera
from kinematics import Kinematics
from servo_control import ServoControl
from config import *

class Tracker:
    def __init__(self):
        self.config = globals()
        self.camera = Camera(self.config)
        self.kinematics = Kinematics(self.config)
        self.servo = ServoControl(self.config)
        self.servo.open_gripper()
        self.last_position = None
        self.stationary_start = None

    def pixel_to_world(self, x, y, z):
        # Convert pixel coordinates to world coordinates (meters)
        # Camera center is at (FRAME_WIDTH/2, FRAME_HEIGHT/2)
        x_world = (x - self.config['FRAME_WIDTH'] / 2) * z / self.config['FOCAL_LENGTH']
        y_world = (y - self.config['FRAME_HEIGHT'] / 2) * z / self.config['FOCAL_LENGTH']
        z_world = z
        return x_world, y_world, z_world

    def run(self):
        try:
            while True:
                x, y, z = self.camera.get_object_position()
                if x is None:
                    print("Object not detected")
                    self.last_position = None
                    self.stationary_start = None
                    continue

                # Convert to world coordinates
                x_world, y_world, z_world = self.pixel_to_world(x, y, z)
                print(f"Object position: ({x_world:.2f}, {y_world:.2f}, {z_world:.2f}) m")

                # Check workspace
                if np.sqrt(x_world**2 + y_world**2 + z_world**2) > self.config['WORKSPACE_RADIUS']:
                    print("Object outside workspace")
                    self.last_position = None
                    self.stationary_start = None
                    continue

                # Compute servo angles
                angles = self.kinematics.inverse_kinematics(x_world, y_world, z_world)
                if angles is None:
                    print("Unreachable position")
                    continue

                # Move arm
                if not self.servo.set_arm_angles(angles):
                    print("Invalid angles")
                    continue

                # Check if object is stationary
                current_position = np.array([x, y, z])
                if self.last_position is not None:
                    movement = np.linalg.norm(current_position - self.last_position)
                    if movement < self.config['STATIONARY_THRESHOLD']:
                        if self.stationary_start is None:
                            self.stationary_start = time.time()
                        elif time.time() - self.stationary_start >= self.config['STATIONARY_TIME']:
                            print("Object stationary, grabbing")
                            self.servo.close_gripper()
                            time.sleep(self.config['GRIPPER_HOLD_TIME'])
                            self.servo.open_gripper()
                            self.stationary_start = None
                    else:
                        self.stationary_start = None
                self.last_position = current_position

                # Center error
                error_x = x - self.config['FRAME_WIDTH'] / 2
                error_y = y - self.config['FRAME_HEIGHT'] / 2
                if abs(error_x) < self.config['CENTER_THRESHOLD'] and abs(error_y) < self.config['CENTER_THRESHOLD']:
                    print("Object centered")
                else:
                    print(f"Centering error: ({error_x:.0f}, {error_y:.0f}) pixels")

                time.sleep(0.1)  # ~10 FPS

        finally:
            self.camera.release()
            self.servo.open_gripper()

if __name__ == "__main__":
    tracker = Tracker()
    tracker.run()