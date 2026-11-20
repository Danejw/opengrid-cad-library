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

  // Preserve mechanical face contrast without the previous emissive washout.
  const material = useMemo(() => {
    const color = new THREE.Color(model.accent);
    color.lerp(new THREE.Color(lightMode ? '#365466' : '#426276'), lightMode ? 0.35 : 0.25);
    return new THREE.MeshStandardMaterial({
      color,
      metalness: 0.03,
      roughness: 0.8,
      flatShading: true,
      wireframe,
      side: THREE.DoubleSide,
      polygonOffset: true,
      polygonOffsetFactor: 1,
      polygonOffsetUnits: 1,
    });
  }, [lightMode, model.accent, wireframe]);
  useEffect(() => () => material.dispose(), [material]);

  // Thin crease lines at sharp angles reveal the actual source CAD profile.
  const edgeMaterial = useMemo(() => new THREE.LineBasicMaterial({
    color: lightMode ? '#223946' : '#183743',
    transparent: true,
    opacity: lightMode ? 0.38 : 0.46,
    depthTest: true,
    depthWrite: false,
  }), [lightMode]);
  useEffect(() => () => edgeMaterial.dispose(), [edgeMaterial]);

  const prepared = useMemo(() => {
    const object = scene.clone(true);
    const edgeGeometries: THREE.EdgesGeometry[] = [];
    object.traverse((node) => {
      if (!(node instanceof THREE.Mesh)) return;
      if (!node.geometry.getAttribute('normal')) node.geometry.computeVertexNormals();
      node.material = material;
      node.castShadow = false;
      node.receiveShadow = false;
      if (!wireframe) {
        const edges = new THREE.EdgesGeometry(node.geometry, 38);
        edgeGeometries.push(edges);
        const lines = new THREE.LineSegments(edges, edgeMaterial);
        lines.renderOrder = 1;
        node.add(lines);
      }
    });
    return { object, edgeGeometries };
  }, [scene, material, edgeMaterial, wireframe]);
  useEffect(() => () => {
    prepared.edgeGeometries.forEach((geometry) => geometry.dispose());
  }, [prepared]);

  // Source meshes use millimetres and Z-up. Display in Three.js Y-up.
  return <Center><group rotation={[-Math.PI / 2, 0, 0]}><primitive object={prepared.object} /></group></Center>;
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
      onCreated={({ gl }) => { gl.toneMappingExposure = 0.9; }}
      aria-label={`Interactive 3D model of ${model.name}. Drag to orbit and scroll or pinch to zoom.`}
    >
      <ambientLight intensity={0.45} />
      <hemisphereLight intensity={0.85} groundColor={lightMode ? '#809595' : '#253f4a'} color="#f5f9ff" />
      <directionalLight position={[110, 145, 95]} intensity={1.6} color="#ffffff" />
      <directionalLight position={[-105, 65, -115]} intensity={0.55} color="#b9def0" />
      <directionalLight position={[20, -90, 80]} intensity={0.22} color="#d3f5e9" />
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
