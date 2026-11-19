"""Topology-preserving 3MF packaging for pinned native OpenSCAD geometry.

Some OpenSCAD STL exports include detached zero-area triangular sheets.
STL does not preserve mesh vertex topology. Require exactly one closed solid;
discard ONLY isolated zero-area, zero-volume sheets, preserving the original
solid's vertices and faces. Verify identical bounding box and volume before
publishing a canonical printable 3MF file. No rescaling or remeshing.
"""
from __future__ import annotations
import math
from pathlib import Path
import trimesh
import numpy as np


def convert_native_stl_to_3mf(raw_stl: Path, output_3mf: Path) -> dict:
    raw_stl, output_3mf = Path(raw_stl), Path(output_3mf)
    original = trimesh.load_mesh(raw_stl, process=True)
    if not isinstance(original, trimesh.Trimesh):
        raise ValueError(f"Expected a single mesh: {raw_stl}")
    pieces = original.split(only_watertight=False)
    solids = [m for m in pieces if m.is_watertight and m.is_volume and m.volume > 1e-4]
    flakes = [m for m in pieces if not (m.is_watertight and m.is_volume and m.volume > 1e-4)]
    if len(solids) != 1:
        raise ValueError(f"Expected exactly one closed native body, got {len(solids)} in {raw_stl}")
    if any(abs(m.volume) > 1e-9 or m.area > 1e-6 for m in flakes):
        raise ValueError(f"Non-degenerate source geometry would be discarded: {raw_stl}")
    native = solids[0]
    if not (native.is_watertight and native.is_volume and native.volume > 0):
        raise ValueError(f"Native solid is not closed: {raw_stl}")
    if not np.allclose(native.bounds, original.bounds, rtol=0, atol=1e-5):
        raise ValueError(f"Native bounds differ from source: {raw_stl}")
    if not math.isclose(native.volume, original.volume, rel_tol=1e-7, abs_tol=1e-4):
        raise ValueError(f"Native volume differs from source: {raw_stl}")
    output_3mf.parent.mkdir(parents=True, exist_ok=True)
    native.export(output_3mf)
    verified = trimesh.load_mesh(output_3mf, process=True)
    if not isinstance(verified, trimesh.Trimesh) or not (
        verified.is_watertight and verified.is_volume and verified.volume > 0
    ):
        raise ValueError(f"3MF export lost its native topology: {output_3mf}")
    if not np.allclose(verified.bounds, native.bounds, rtol=0, atol=1e-5):
        raise ValueError(f"3MF bounds changed: {output_3mf}")
    if not math.isclose(verified.volume, native.volume, rel_tol=1e-7, abs_tol=1e-4):
        raise ValueError(f"3MF volume changed: {output_3mf}")
    return {
        "native_3mf": str(output_3mf),
        "source_triangles": len(original.faces),
        "closed_native_triangles": len(native.faces),
        "discarded_zero_area_triangles": sum(len(m.faces) for m in flakes),
        "source_volume_mm3": round(float(original.volume), 5),
        "output_volume_mm3": round(float(verified.volume), 5),
        "topology_preserved": True,
        "physical_fit_verified": False
    }
