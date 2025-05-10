import numpy as np
from scipy.optimize import minimize

class RobotArm5DOF:
    def __init__(self, dh_params=None):
        # DH parameters: [a, alpha, d, theta]
        self.dh_params = dh_params if dh_params is not None else [
            [0, np.pi/2, 0.1, 0],       # Joint 1
            [0.2, 0, 0, 0],             # Joint 2
            [0.2, 0, 0, 0],             # Joint 3
            [0, np.pi/2, 0, 0],         # Joint 4
            [0, 0, 0.1, 0]              # Joint 5
        ]
        self.joint_limits = [
            [-np.pi, np.pi],            # Joint 1
            [-np.pi/2, np.pi/2],        # Joint 2
            [-np.pi/2, np.pi/2],        # Joint 3
            [-np.pi, np.pi],            # Joint 4
            [-np.pi, np.pi],            # Joint 5
        ]
    
    def transform_matrix(self, params):
        a, alpha, d, theta = params
        return np.array([
            [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
            [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])
    
    def forward_kinematics(self, theta_values):
        # Update DH parameters with current joint angles
        current_dh = np.copy(self.dh_params)
        for i in range(len(theta_values)):
            current_dh[i][3] = theta_values[i]
        
        # Calculate transformation matrices
        T = np.eye(4)
        for params in current_dh:
            T = T @ self.transform_matrix(params)
        
        # Extract position and orientation
        position = T[:3, 3]
        orientation = np.array([
            np.arctan2(T[2, 1], T[2, 2]),  # Roll
            np.arctan2(-T[2, 0], np.sqrt(T[2, 1]**2 + T[2, 2]**2)),  # Pitch
            np.arctan2(T[1, 0], T[0, 0])   # Yaw
        ])
        
        return position, orientation, T
    
    def inverse_kinematics(self, target_pos, target_orient=None, initial_guess=None):
        if initial_guess is None:
            initial_guess = np.zeros(5)
        
        # Objective function to minimize distance
        def objective(thetas):
            # Apply joint limits
            for i, theta in enumerate(thetas):
                if theta < self.joint_limits[i][0] or theta > self.joint_limits[i][1]:
                    return 1e6  # Return high value for out-of-bounds
            
            pos, orient, _ = self.forward_kinematics(thetas)
            
            # Calculate position error
            pos_error = np.linalg.norm(pos - target_pos)
            
            # Add orientation error if provided
            if target_orient is not None:
                orient_error = np.linalg.norm(orient - target_orient)
                return pos_error + orient_error
            
            return pos_error
        
        # Use optimization algorithm to find solution
        result = minimize(objective, initial_guess, method='BFGS')
        
        # Clip results to joint limits for safety
        solution = np.clip(result.x, 
                           [limit[0] for limit in self.joint_limits],
                           [limit[1] for limit in self.joint_limits])
        
        return solution
    
    def get_joint_positions(self, theta_values):
        # Calculate all joint positions for visualization
        positions = []
        current_dh = np.copy(self.dh_params)
        
        for i in range(len(theta_values)):
            current_dh[i][3] = theta_values[i]
        
        T = np.eye(4)
        positions.append(T[:3, 3].copy())  # Base position
        
        for params in current_dh:
            T = T @ self.transform_matrix(params)
            positions.append(T[:3, 3].copy())
        
        return positions
