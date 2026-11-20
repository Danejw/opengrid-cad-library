#!/usr/bin/env python3
"""Hash-check publisher originals and stage 3MF meshes for the local 3D viewer."""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]
def stage(root: Path = ROOT) -> list[dict]:
    manifest = json.loads((root / "vendor/opengrid-sources/imported-manifest.json").read_text())
    output = root / "output/publisher_samples"
    output.mkdir(parents=True, exist_ok=True)
    records=[]
    for model in manifest["imports"]:
        src=root / model["path"]
        data=src.read_bytes()
        if len(data)!=model["size"] or hashlib.sha256(data).hexdigest()!=model["sha256"]:
            raise ValueError(f"Publisher original mismatch: {src}")
        mesh=trimesh.load_mesh(src, process=True)
        if not isinstance(mesh,trimesh.Trimesh) or not mesh.is_watertight or not mesh.is_volume or mesh.volume<=0:
            raise ValueError(f"Invalid publisher source mesh: {src}")
        if any(not 0 < float(dim) < 300 for dim in mesh.extents):
            raise ValueError(f"Unexpected publisher mesh dimensions: {src}: {mesh.extents}")
        shutil.copyfile(src,output/src.name)
        records.append({"id":model["id"],"name":src.name,"sha256":model["sha256"],"faces":len(mesh.faces)})
    (output / "provenance.json").write_text(json.dumps(records,indent=2)+"\n",encoding="utf-8")
    return records
if __name__=="__main__":
    print("Original publisher meshes staged:",len(stage()))
