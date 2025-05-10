// robot-model.js
class RobotArm {
    constructor(scene) {
      this.scene = scene;
      this.links = [];
      this.joints = [];
  
      // Robot dimensions and colors
      const baseColor = 0x444444;
      const jointColor = 0x2288cc;
      const linkColor = 0x999999;
      
      // Create base
      const baseGeometry = new THREE.CylinderGeometry(0.1, 0.1, 0.05, 32);
      const baseMaterial = new THREE.MeshPhongMaterial({ color: baseColor });
      this.base = new THREE.Mesh(baseGeometry, baseMaterial);
      this.base.position.set(0, 0, 0);
      this.scene.add(this.base);
      
      // Create joints and links
      const jointGeometry = new THREE.SphereGeometry(0.035, 32, 32);
      const jointMaterial = new THREE.MeshPhongMaterial({ color: jointColor });
      
      // DH parameters (simplified version for visualization)
      this.dhParams = [
        [0, Math.PI/2, 0.1, 0],     // Joint 1
        [0.2, 0, 0, 0],             // Joint 2
        [0.2, 0, 0, 0],             // Joint 3
        [0, Math.PI/2, 0, 0],       // Joint 4
        [0, 0, 0.1, 0]              // Joint 5
      ];
      
      // Create joints
      for (let i = 0; i < 5; i++) {
        const joint = new THREE.Mesh(jointGeometry, jointMaterial);
        this.joints.push(joint);
        this.scene.add(joint);
        
        // Create link (except for the last joint)
        if (i < 4) {
          const linkGeometry = new THREE.CylinderGeometry(0.02, 0.02, 0.2, 16);
          const linkMaterial = new THREE.MeshPhongMaterial({ color: linkColor });
          const link = new THREE.Mesh(linkGeometry, linkMaterial);
          this.links.push(link);
          this.scene.add(link);
        }
      }
      
      // Create end effector
      const eeGeometry = new THREE.ConeGeometry(0.03, 0.08, 16);
      const eeMaterial = new THREE.MeshPhongMaterial({ color: 0xff6666 });
      this.endEffector = new THREE.Mesh(eeGeometry, eeMaterial);
      this.scene.add(this.endEffector);
      
      // Initial position
      this.updatePositions([0, 0, 0, 0, 0]);
    }
    
    updatePositions(jointPositions) {
      // Convert array of positions to THREE.Vector3 objects
      const positions = jointPositions.map(pos => {
        if (Array.isArray(pos)) {
          return new THREE.Vector3(pos[0], pos[2], pos[1]); // Adjust coordinates for visualization
        }
        return pos;
      });
      
      // Update joint positions
      for (let i = 0; i < positions.length - 1; i++) {
        this.joints[i].position.copy(positions[i]);
        
        // Update link position and orientation
        if (i < positions.length - 2) {
          const link = this.links[i];
          const start = positions[i];
          const end = positions[i + 1];
          const midpoint = new THREE.Vector3().addVectors(start, end).multiplyScalar(0.5);
          
          // Set link position to midpoint
          link.position.copy(midpoint);
          
          // Orient link to point from start to end
          const direction = new THREE.Vector3().subVectors(end, start);
          const length = direction.length();
          
          // Scale link length
          link.scale.set(1, length / 0.2, 1);
          
          // Rotate link to align with direction
          if (length > 0.001) {
            const arrow = new THREE.ArrowHelper(direction.clone().normalize(), start);
            link.quaternion.copy(arrow.quaternion);
            arrow.dispose();
          }
        }
      }
      
      // Update end effector position
      if (positions.length > 0) {
        this.endEffector.position.copy(positions[positions.length - 1]);
        
        // Point end effector outward from the last link
        if (positions.length > 1) {
          const direction = new THREE.Vector3().subVectors(
            positions[positions.length - 1],
            positions[positions.length - 2]
          );
          if (direction.length() > 0.001) {
            const arrow = new THREE.ArrowHelper(direction.clone().normalize(), positions[positions.length - 1]);
            this.endEffector.quaternion.copy(arrow.quaternion);
            arrow.dispose();
          }
        }
      }
    }
  }