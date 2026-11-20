#!/usr/bin/env python3
"""Validate untouched publisher-authored board models and stage their originals.

The 3MF and STEP originals remain byte-for-byte identical to David D's files.
This code never infers or generates their physical geometry.
"""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "vendor" / "davidd-opengrid" / "manifest.json"


def validate_and_stage(root: Path = ROOT) -> list[dict]:
    manifest = json.loads((root / "vendor/davidd-opengrid/manifest.json").read_text())
    source_files = {f["path"]: f for f in manifest["files"]}
    dest = root / "output/official"
    dest.mkdir(parents=True, exist_ok=True)
    for item in manifest["files"]:
        source = root / item["path"]
        data = source.read_bytes()
        if len(data) != item["size"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"Official publisher file changed: {source}")
        shutil.copyfile(source, dest / source.name)

    records = []
    for board in manifest["boards"]:
        item = source_files[board["source_file"]]
        source = root / item["path"]
        mesh = trimesh.load_mesh(source, process=True)
        if not isinstance(mesh, trimesh.Trimesh) or len(mesh.faces) < 40:
            raise ValueError(f"Cannot read official board mesh: {source}")
        if not mesh.is_watertight or not mesh.is_volume or mesh.volume <= 0:
            raise ValueError(f"Official board is not a closed volume: {source}")
        extents = sorted(float(x) for x in mesh.extents)
        pitch = board["cells"] * 28.0
        if not all(abs(e - pitch) < 6 for e in extents[1:]):
            raise ValueError(f"Official board size mismatch: {source}: {extents}")
        if not 1.0 < extents[0] < 16.0:
            raise ValueError(f"Official board thickness implausible: {source}: {extents}")
        records.append({"part": source.stem, "sha256": item["sha256"], "faces": len(mesh.faces),
                        "bounds_mm": [round(float(x), 3) for x in mesh.extents],
                        "source": item["path"]})
    (dest / "origin_manifest.json").write_text(json.dumps(records, indent=2) + "\n")
    return records


if __name__ == "__main__":
    records = validate_and_stage()
    print(f"Verified and staged {len(records)} official openGrid boards and original STEP files")
