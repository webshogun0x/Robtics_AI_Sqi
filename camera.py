# camera.py
import cv2
import numpy as np

class Camera:
    def __init__(self, config):
        self.config = config
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    def get_object_position(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None, None

        # Convert to HSV for color-based detection (e.g., red ball)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, None, None

        # Get largest contour
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) < 100:  # Ignore small contours
            return None, None, None

        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2

        # Estimate distance (z) using known object size
        z = (self.config.FOCAL_LENGTH * self.config.KNOWN_OBJECT_SIZE) / w

        return center_x, center_y, z

    def release(self):
        self.cap.release()