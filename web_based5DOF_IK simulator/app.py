from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from robot_arm_ik import RobotArm5DOF  # Import the IK solver we created earlier

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the robot model
robot = RobotArm5DOF()

@app.route('/api/solve-ik', methods=['POST'])
def solve_ik():
    try:
        # Get target position from request
        data = request.json
        target_position = np.array([
            data.get('x', 0.3),
            data.get('y', 0.2),
            data.get('z', 0.3)
        ])
        
        # Optional parameters
        initial_guess = np.array(data.get('initial_guess', [0, 0, 0, 0, 0]))
        
        # Solve inverse kinematics
        joint_angles = robot.inverse_kinematics(target_position, initial_guess=initial_guess)
        
        # Get joint positions for visualization
        joint_positions = robot.get_joint_positions(joint_angles)
        
        # Convert numpy arrays to lists for JSON serialization
        result = {
            'joint_angles': joint_angles.tolist(),
            'joint_positions': [pos.tolist() for pos in joint_positions],
            'target_position': target_position.tolist(),
            'success': True
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/forward-kinematics', methods=['POST'])
def forward_kinematics():
    try:
        # Get joint angles from request
        data = request.json
        joint_angles = np.array(data.get('joint_angles', [0, 0, 0, 0, 0]))
        
        # Calculate forward kinematics
        position, orientation, _ = robot.forward_kinematics(joint_angles)
        
        # Get joint positions for visualization
        joint_positions = robot.get_joint_positions(joint_angles)
        
        # Convert numpy arrays to lists for JSON serialization
        result = {
            'position': position.tolist(),
            'orientation': orientation.tolist(),
            'joint_positions': [pos.tolist() for pos in joint_positions],
            'success': True
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)