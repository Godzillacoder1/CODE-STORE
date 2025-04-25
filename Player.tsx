import { useRef, useState, useCallback } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { useKeyboardControls } from '@react-three/drei';
import * as THREE from 'three';
import { useGameStore } from '../store/gameStore';

export function Player() {
  const playerRef = useRef<THREE.Group>(null);
  const gunRef = useRef<THREE.Group>(null);
  const [, getKeys] = useKeyboardControls();
  const { camera } = useThree();
  const speed = 0.15;
  const jumpForce = 0.3;
  const gravity = 0.01;
  const [velocity, setVelocity] = useState(new THREE.Vector3());
  const [isJumping, setIsJumping] = useState(false);
  const direction = new THREE.Vector3();
  const frontVector = new THREE.Vector3();
  const sideVector = new THREE.Vector3();
  
  const shoot = useCallback(() => {
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(new THREE.Vector2(0, 0), camera);
    
    const bullet = new THREE.Mesh(
      new THREE.SphereGeometry(0.1),
      new THREE.MeshBasicMaterial({ color: '#ffff00' })
    );
    
    bullet.position.copy(camera.position);
    const bulletVelocity = raycaster.ray.direction.multiplyScalar(1);
    
    return { bullet, velocity: bulletVelocity };
  }, [camera]);
  
  useFrame((state) => {
    if (!playerRef.current || !gunRef.current) return;

    const keyboard = getKeys();
    
    // Movement direction based on camera
    frontVector.set(0, 0, Number(keyboard.backward) - Number(keyboard.forward));
    sideVector.set(Number(keyboard.left) - Number(keyboard.right), 0, 0); // Fixed A/D controls
    direction
      .subVectors(frontVector, sideVector)
      .normalize()
      .multiplyScalar(speed)
      .applyEuler(state.camera.rotation);
    
    // Apply movement
    playerRef.current.position.x += direction.x;
    playerRef.current.position.z += direction.z;
    
    // Apply gravity
    setVelocity(v => new THREE.Vector3(
      v.x,
      Math.max(v.y - gravity, -1),
      v.z
    ));

    // Jump
    if (keyboard.jump && !isJumping) {
      setVelocity(v => new THREE.Vector3(v.x, jumpForce, v.z));
      setIsJumping(true);
    }

    // Ground check
    if (playerRef.current.position.y <= 1) {
      playerRef.current.position.y = 1;
      setVelocity(v => new THREE.Vector3(v.x, 0, v.z));
      setIsJumping(false);
    }

    // Apply velocity
    playerRef.current.position.add(velocity);

    // Update camera
    state.camera.position.copy(playerRef.current.position);
    state.camera.position.y += 1.5;

    // Update gun position
    gunRef.current.position.copy(state.camera.position);
    gunRef.current.rotation.copy(state.camera.rotation);
    gunRef.current.position.x += Math.sin(state.camera.rotation.y) * 0.4;
    gunRef.current.position.z += Math.cos(state.camera.rotation.y) * 0.4;
    gunRef.current.position.y -= 0.3;
    gunRef.current.rotation.x += 0.2;
  });

  return (
    <>
      <group ref={playerRef}>
        <mesh position={[0, 1, 0]}>
          <capsuleGeometry args={[0.3, 1, 4, 8]} />
          <meshStandardMaterial color="#4a9eff" />
        </mesh>
      </group>
      <group ref={gunRef}>
        <mesh position={[0.15, -0.1, -0.3]} rotation={[0, Math.PI / 2, 0]}>
          <boxGeometry args={[0.6, 0.1, 0.1]} />
          <meshStandardMaterial color="#333333" metalness={0.8} roughness={0.2} />
        </mesh>
        <mesh position={[0, -0.05, -0.2]}>
          <boxGeometry args={[0.1, 0.2, 0.1]} />
          <meshStandardMaterial color="#222222" metalness={0.8} roughness={0.2} />
        </mesh>
      </group>
    </>
  );
}