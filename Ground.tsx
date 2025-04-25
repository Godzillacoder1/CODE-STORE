import * as THREE from 'three';
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export function Ground() {
  const groundRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (!groundRef.current) return;
    const time = state.clock.getElapsedTime();
    groundRef.current.material.uniforms.time.value = time;
  });

  return (
    <mesh 
      ref={groundRef}
      rotation={[-Math.PI / 2, 0, 0]} 
      position={[0, 0, 0]}
    >
      <planeGeometry args={[100, 100, 32, 32]} />
      <shaderMaterial
        uniforms={{
          time: { value: 0 },
          color: { value: new THREE.Color('#4a5568') },
        }}
        vertexShader={`
          uniform float time;
          varying vec2 vUv;
          
          void main() {
            vUv = uv;
            vec3 pos = position;
            pos.z += sin(pos.x * 0.5 + time * 0.5) * 0.2 * smoothstep(0.0, 0.2, abs(pos.x) / 50.0);
            pos.z += sin(pos.y * 0.5 + time * 0.5) * 0.2 * smoothstep(0.0, 0.2, abs(pos.y) / 50.0);
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
          }
        `}
        fragmentShader={`
          uniform vec3 color;
          varying vec2 vUv;
          
          void main() {
            float grid = abs(fract(vUv.x * 20.0 - 0.5) - 0.5) + abs(fract(vUv.y * 20.0 - 0.5) - 0.5);
            grid = smoothstep(0.9, 0.95, grid);
            vec3 finalColor = mix(color, color * 1.5, grid);
            gl_FragColor = vec4(finalColor, 1.0);
          }
        `}
      />
    </mesh>
  );
}