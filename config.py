# config.py
# Camera settings
CAMERA_INDEX = 0  # USB camera index
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FOCAL_LENGTH = 700  # Calibrated focal length (pixels)
KNOWN_OBJECT_SIZE = 0.05  # Real-world object size (meters, e.g., 5 cm ball)

# Arm settings
ARM_MAX_REACH = 0.5  # Max reach in meters
WORKSPACE_RADIUS = 0.5  # Hemispherical workspace radius
SERVO_CHANNELS = [0, 1, 2, 3, 4, 5]  # PCA9685 channels for base, shoulder, elbow, wrist pitch, wrist roll, gripper
SERVO_MIN_PULSE = 500  # µs
SERVO_MAX_PULSE = 2500  # µs
SERVO_ANGLE_RANGE = 180  # Degrees
GRIPPER_OPEN_ANGLE = 0  # Degrees
GRIPPER_CLOSED_ANGLE = 90  # Degrees

# Tracking settings
CENTER_THRESHOLD = 50  # Pixels (tolerance for centering)
STATIONARY_THRESHOLD = 10  # Pixels (movement threshold)
STATIONARY_TIME = 3  # Seconds
GRIPPER_HOLD_TIME = 5  # Seconds