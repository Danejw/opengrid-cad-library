"""Validate a native-connector accessory mesh; never infer physical fit."""
from __future__ import annotations
import json
from pathlib import Path
from validate_interfaces import inspect_mesh

def main():
    folder=Path("output/accessories")
    target=folder/"opengrid_openconnect_cable_hook.stl"
    if not target.exists():
        raise SystemExit("Phase 2 accessory wasn't generated")
    report=inspect_mesh(target)
    # A cable hook must be bonded to the receiver as a single connected body.
    import trimesh
    mesh=trimesh.load_mesh(target,process=True)
    count=len(mesh.split(only_watertight=False))
    if count!=1:
        raise SystemExit(f"Expected one fused watertight cable hook, got {count} bodies")
    report["connected_components"]=count
    report["cad_valid"]=True
    report["fit_verified"]=False
    report["slicer_verified"]=False
    report["load_tested"]=False
    (folder/"verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__":main()
