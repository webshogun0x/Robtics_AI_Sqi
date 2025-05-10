// main.js
// API function to solve IK
function solveIK(targetPosition) {
  return fetch("http://localhost:5000/api/solve-ik", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      x: targetPosition[0],
      y: targetPosition[1],
      z: targetPosition[2],
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (!data.success) {
        throw new Error(data.error || "IK solver failed");
      }
      return data.joint_positions;
    })
    .catch((error) => {
      console.error("Error solving IK:", error);
      // Fallback to a default position if API fails
      console.log("Using fallback positions");
      return defaultPositions(targetPosition);
    });
}

// Fallback function in case the API is unreachable
function defaultPositions(targetPosition) {
  const basePos = [0, 0, 0];
  const joint1 = [0, 0, 0.1];
  const joint2 = [
    targetPosition[0] * 0.2,
    targetPosition[1] * 0.2,
    0.1 + targetPosition[2] * 0.1,
  ];
  const joint3 = [
    targetPosition[0] * 0.4,
    targetPosition[1] * 0.4,
    0.1 + targetPosition[2] * 0.2,
  ];
  const joint4 = [
    targetPosition[0] * 0.5,
    targetPosition[1] * 0.5,
    0.1 + targetPosition[2] * 0.3,
  ];
  const endPoint = targetPosition;

  return [basePos, joint1, joint2, joint3, joint4, endPoint];
}

// Scene setup
let scene, camera, renderer, robotArm;
let targetPosition = [0.3, 0.2, 0.3];
let targetMesh;

function init() {
  // Create scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf0f0f0);

  // Create camera
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(0.7, 0.7, 0.7);
  camera.lookAt(0, 0.2, 0);

  // Create renderer
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  document.body.appendChild(renderer.domElement);

  // Add lights
  const ambientLight = new THREE.AmbientLight(0x666666);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(1, 1, 1);
  directionalLight.castShadow = true;
  scene.add(directionalLight);

  // Add grid for reference
  const gridHelper = new THREE.GridHelper(1, 10);
  scene.add(gridHelper);

  // Create coordinate axes
  const axesHelper = new THREE.AxesHelper(0.3);
  scene.add(axesHelper);

  // Create robot arm
  robotArm = new RobotArm(scene);

  // Create target indicator
  const targetGeometry = new THREE.SphereGeometry(0.02, 16, 16);
  const targetMaterial = new THREE.MeshBasicMaterial({
    color: 0xff0000,
    transparent: true,
    opacity: 0.7,
  });
  targetMesh = new THREE.Mesh(targetGeometry, targetMaterial);
  targetMesh.position.set(
    targetPosition[0],
    targetPosition[2],
    targetPosition[1]
  ); // Adjust coordinates
  scene.add(targetMesh);

  // Set up UI controls
  setupControls();

  // Handle window resize
  window.addEventListener("resize", onWindowResize);

  // Initial IK solve
  updateTarget(targetPosition);

  // Start animation loop
  animate();
}

function setupControls() {
  // Set up slider controls
  const xSlider = document.getElementById("x-slider");
  const ySlider = document.getElementById("y-slider");
  const zSlider = document.getElementById("z-slider");
  const xValue = document.getElementById("x-value");
  const yValue = document.getElementById("y-value");
  const zValue = document.getElementById("z-value");

  xSlider.addEventListener("input", () => {
    targetPosition[0] = parseFloat(xSlider.value);
    xValue.textContent = targetPosition[0].toFixed(2);
    updateTarget(targetPosition);
  });

  ySlider.addEventListener("input", () => {
    targetPosition[1] = parseFloat(ySlider.value);
    yValue.textContent = targetPosition[1].toFixed(2);
    updateTarget(targetPosition);
  });

  zSlider.addEventListener("input", () => {
    targetPosition[2] = parseFloat(zSlider.value);
    zValue.textContent = targetPosition[2].toFixed(2);
    updateTarget(targetPosition);
  });
}

function updateTarget(position) {
  // Update target visual indicator
  targetMesh.position.set(position[0], position[2], position[1]); // Adjust coordinates

  // Solve IK
  solveIK(position).then((jointPositions) => {
    robotArm.updatePositions(jointPositions);
  });
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

// Initialize the app when everything is loaded
window.addEventListener("DOMContentLoaded", init);
