#!/usr/bin/env python3
"""Hash-check and stage the exact original David D accessory meshes."""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]

def validate_and_stage(root: Path = ROOT) -> list[dict]:
    manifest = json.loads((root / "vendor/davidd-opengrid/accessories-manifest.json").read_text())
    files = {f["path"]: f for f in manifest["files"]}
    out = root / "output/official_accessories"
    out.mkdir(parents=True, exist_ok=True)
    for entry in manifest["files"]:
        src = root / entry["path"]
        data = src.read_bytes()
        if len(data) != entry["size"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError(f"Publisher accessory file changed: {src}")
        shutil.copyfile(src, out / src.name)
    results = []
    for model in manifest["models"]:
        src = root / model["source_file"]
        mesh = trimesh.load_mesh(src, process=True)
        if not isinstance(mesh, trimesh.Trimesh) or len(mesh.faces) < 20:
            raise ValueError(f"Missing or unparseable official accessory geometry: {src}")
        if not mesh.is_watertight or not mesh.is_volume or mesh.volume <= 0:
            raise ValueError(f"Invalid original publisher mesh: {src}")
        extents = [float(x) for x in mesh.extents]
        if any(x <= 0 or x >= 300 for x in extents):
            raise ValueError(f"Implausible original accessory dimensions: {src} {extents}")
        results.append({"id": model["id"], "part": src.stem, "faces": len(mesh.faces), "bounds_mm": extents,
                        "sha256": files[model["source_file"]]["sha256"]})
    (out / "origin_manifest.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results

if __name__ == "__main__":
    print("Validated official accessories:", len(validate_and_stage()))
