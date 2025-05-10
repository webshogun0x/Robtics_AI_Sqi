# Systems  Overview

## Requirements

* ## Object detection

  * Use the USB camera to detect a specific object (e.g., a red  or green colored box ).
  * Identify the object’s position (x, y) and approximate distance (z) in the camera frame.
  
* ## Arm control

  * djust servo motor angles to keep the object centered in the camera frame.
  * Use inverse kinematics to compute joint angles based on the object’s 3D position.
  
* ## Distance tracking

  * Estimate the object’s distance from the camera (e.g., via object size or depth estimation).
  * Determine if the object is outside the arm’s workspace (e.g., too far or unreachable).

* ## Gripper Action

  * If the object is stationary for 3 seconds, close the gripper to grab it.
  * Hold for 5 seconds, then open the gripper to release it.

* ## Feedback

  * Log or display status (e.g., object position, arm status, workspace violation).

