import { Component, Suspense, useEffect, useMemo, type ReactNode } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { Center, Html, OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import type { StudioModel } from '../data/types';
import { assetUrl } from '../data/types';

export type ViewDirection = 'iso' | 'front' | 'top' | 'right';

class ModelErrorBoundary extends Component<{
  children: ReactNode;
  onFailure: (error: string) => void;
}, { failed: boolean }> {
  constructor(props: { children: ReactNode; onFailure: (error: string) => void }) {
    super(props);
    this.state = { failed: false };
  }
  static getDerivedStateFromError(): { failed: boolean } {
    return { failed: true };
  }
  componentDidCatch(error: Error): void {
    this.props.onFailure(error.message);
  }
  render(): ReactNode {
    return this.state.failed ? null : this.props.children;
  }
}

function DisplayObject({ model, wireframe, lightMode }: {
  model: StudioModel;
  wireframe: boolean;
  lightMode: boolean;
}) {
  const { scene } = useGLTF(assetUrl(model.model));

  // A softly emissive, matte CAD material guarantees legible color even on
  // mobile GPUs where a face receives very little direct illumination.
  const material = useMemo(() => {
    const color = new THREE.Color(model.accent);
    if (lightMode) color.lerp(new THREE.Color('#2b4c55'), 0.2);
    return new THREE.MeshStandardMaterial({
      color,
      emissive: color,
      emissiveIntensity: 0.24,
      metalness: 0.04,
      roughness: 0.58,
      wireframe,
      side: THREE.DoubleSide,
    });
  }, [lightMode, model.accent, wireframe]);

  useEffect(() => () => material.dispose(), [material]);

  const object = useMemo(() => {
    const clone = scene.clone(true);
    clone.traverse((node) => {
      if (node instanceof THREE.Mesh) {
        // GLB exports may omit NORMAL; compute it once on the shared geometry.
        if (!node.geometry.getAttribute('normal')) node.geometry.computeVertexNormals();
        node.material = material;
        // CAD inspection needs consistent visibility, even on back-facing parts.
        node.castShadow = false;
        node.receiveShadow = false;
      }
    });
    return clone;
  }, [scene, material]);

  // Trimesh exports preserve millimetres and Z-up. Rotate to Three.js Y-up.
  return <Center><group rotation={[-Math.PI / 2, 0, 0]}><primitive object={object} /></group></Center>;
}

function CameraPosition({ model, view, resetVersion }: {
  model: StudioModel;
  view: ViewDirection;
  resetVersion: number;
}) {
  const { camera, controls, invalidate } = useThree();
  useEffect(() => {
    const maxMM = Math.max(...model.boundsInches) * 25.4;
    const distance = Math.max(20, maxMM * 2.45);
    camera.up.set(0, 1, 0);
    if (view === 'top') {
      camera.position.set(0.01, distance, 0);
      camera.up.set(0, 0, -1);
    } else if (view === 'front') {
      camera.position.set(0, 0, distance);
    } else if (view === 'right') {
      camera.position.set(distance, 0, 0);
    } else {
      camera.position.set(distance * 0.82, distance * 0.66, distance * 0.92);
    }
    camera.lookAt(0, 0, 0);
    camera.updateProjectionMatrix();
    if (controls && 'target' in controls && 'update' in controls) {
      const orbit = controls as unknown as { target: THREE.Vector3; update: () => void };
      orbit.target.set(0, 0, 0);
      orbit.update();
    }
    invalidate();
  }, [camera, controls, invalidate, model.id, model.boundsInches, resetVersion, view]);
  return null;
}

export default function ModelViewer({
  model, wireframe, grid, view, resetVersion, rotating, lightMode, onFailure,
}: {
  model: StudioModel;
  wireframe: boolean;
  grid: boolean;
  view: ViewDirection;
  resetVersion: number;
  rotating: boolean;
  lightMode: boolean;
  onFailure: (error: string) => void;
}) {
  return (
    <Canvas
      key={model.id}
      camera={{ fov: 42, near: 0.1, far: 4000, position: [150, 125, 165] }}
      dpr={[1, 1.65]}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      aria-label={`Interactive 3D model of ${model.name}. Drag to orbit and scroll or pinch to zoom.`}
    >
      <ambientLight intensity={0.95} />
      <hemisphereLight intensity={1.55} groundColor={lightMode ? '#829d9c' : '#3d5b62'} color="#fffaf4" />
      <directionalLight position={[120, 170, 130]} intensity={3} color="#fff6e9" />
      <directionalLight position={[-140, 85, -95]} intensity={1.5} color="#b9e5ff" />
      <directionalLight position={[50, -100, -140]} intensity={0.8} color="#d3fff1" />
      {grid && <gridHelper
        args={[400, 40, lightMode ? '#94b3b1' : '#476872', lightMode ? '#c1d2d0' : '#2a454f']}
        position={[0, -Math.max(...model.boundsInches) * 25.4 * 0.58, 0]}
      />}
      <ModelErrorBoundary key={model.id} onFailure={onFailure}>
        <Suspense fallback={<Html center><div className="scene-loader">Loading geometry…</div></Html>}>
          <DisplayObject model={model} wireframe={wireframe} lightMode={lightMode} />
        </Suspense>
      </ModelErrorBoundary>
      <CameraPosition model={model} view={view} resetVersion={resetVersion} />
      <OrbitControls makeDefault enableDamping dampingFactor={0.075} minDistance={5} maxDistance={2200} autoRotate={rotating} autoRotateSpeed={1.2} />
    </Canvas>
  );
}
