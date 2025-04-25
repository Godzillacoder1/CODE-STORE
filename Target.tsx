import { useRef, useState, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useGameStore } from '../store/gameStore';

interface TargetProps {
  position: [number, number, number];
}

export function Target({ position }: TargetProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hit, setHit] = useState(false);
  const [hovered, setHovered] = useState(false);
  const { addScore, addMaterials } = useGameStore();
  const originalPosition = useRef(new THREE.Vector3(...position));
  const time = useRef(Math.random() * Math.PI * 2);

  useFrame((state) => {
    if (!meshRef.current || hit) return;
    
    // Floating animation
    time.current += 0.02;
    meshRef.current.position.y = originalPosition.current.y + Math.sin(time.current) * 0.2;
    
    // Rotation
    meshRef.current.rotation.y += 0.02;
  });

  const handleClick = (event: THREE.Event) => {
    event.stopPropagation();
    if (!hit) {
      setHit(true);
      addScore();
      addMaterials(10);
    }
  };

  if (hit) return null;

  return (
    <mesh
      ref={meshRef}
      position={position}
      onClick={handleClick}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial 
        color={hovered ? '#ff8888' : '#ff4444'}
        roughness={0.3}
        metalness={0.7}
        emissive={hovered ? '#441111' : '#000000'}
      />
    </mesh>
  );
}