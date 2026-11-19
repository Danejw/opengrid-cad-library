"""Machine-check native connector meshes. This is *not* a physical fit test."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import trimesh

def inspect_mesh(path: Path):
    mesh=trimesh.load_mesh(path,process=True)
    if isinstance(mesh,trimesh.Scene):
        mesh=mesh.to_geometry()
    if not isinstance(mesh,trimesh.Trimesh):
        raise ValueError(f"Unsupported mesh type: {path}")
    if len(mesh.vertices)<12 or len(mesh.faces)<12:
        raise ValueError(f"Too few triangles in {path}")
    if not mesh.is_watertight:
        raise ValueError(f"Not watertight: {path}")
    if not mesh.is_winding_consistent:
        raise ValueError(f"Inconsistent winding: {path}")
    if not mesh.is_volume or mesh.volume<=0:
        raise ValueError(f"Invalid enclosed volume: {path}")
    extents=mesh.extents
    if any(e<=0 or e>140 for e in extents):
        raise ValueError(f"Implausible dimensions in mm for {path}: {extents}")
    return {
        "filename":path.name,
        "mesh_valid":True,"watertight":True,
        "volume_mm3":round(float(mesh.volume),3),
        "bounds_mm":[round(float(n),3) for n in extents],
        "triangles":len(mesh.faces),
        "slicer_verified":False,
        "physical_fit_verified":False,
        "load_tested":False
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dir",default="output/interfaces")
    args=ap.parse_args()
    folder=Path(args.dir)
    paths=sorted(folder.glob("*.stl"))
    if len(paths)<3:
        raise SystemExit("Expected 2 original snap variants plus 1 receiver plate")
    results=[inspect_mesh(p) for p in paths]
    (folder/"verification.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))

if __name__=="__main__":main()
