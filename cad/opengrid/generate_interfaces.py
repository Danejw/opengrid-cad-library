"""Render genuine upstream openGrid/openConnect geometry using OpenSCAD.

No custom snap profile is authored here. This is an adapter around unmodified
mitufy/openGrid OpenSCAD sources pinned in vendor/.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "mitufy-opengrid"
SNAP = VENDOR / "opengrid_parametric_snap.scad"
RECEIVER = VENDOR / "openconnect_plate.scad"
PITCH_MM = 28.0

def profile_commands(variant: str):
    if variant not in {"all", "full", "lite"}:
        raise ValueError(f"Unknown variant: {variant}")
    commands = []
    for name, thickness in (("lite", 4.0), ("full", 6.8)):
        if variant in ("all", name):
            commands.append((
                f"opengrid_openconnect_snap_{name}.stl",
                SNAP, {
                    "snap_thickness": thickness,
                    "snap_body_shape": "Directional",
                    "generate_snap": "openConnect",
                    "generate_screw": "None",
                    "view_cross_section": "None",
                    "text_depth": 0
                },
            ))
    commands.append((
        "opengrid_openconnect_receiver_2x1.stl",
        RECEIVER, {
            "plate_size_unit": "grid",
            "plate_horizontal_size": 2,
            "plate_vertical_size": 1,
            "plate_extra_thickness": 1.2,
            "slot_type": "slot",
            "slot_position": "All",
            "slot_lock_distribution": "Corners",
        },
    ))
    return commands

def build(variant="all", output=None, openscad="openscad", dry_run=False):
    dest = Path(output) if output else ROOT / "output" / "interfaces"
    dest.mkdir(parents=True, exist_ok=True)
    results=[]
    for name, script, parameters in profile_commands(variant):
        if not script.is_file():
            raise FileNotFoundError(f"Missing vendored upstream generator: {script}")
        target = dest / name
        cmd = [openscad, "-o", str(target)]
        for key, val in parameters.items():
            cmd += ["-D", f"{key}={json.dumps(val)}"]
        cmd += [str(script)]
        if not dry_run:
            result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
            if result.returncode != 0 or not target.is_file() or target.stat().st_size < 100:
                raise RuntimeError(
                    f"OpenSCAD failed for {name}: exit={result.returncode}\n"
                    f"stdout={result.stdout[-3000:]}\nstderr={result.stderr[-5000:]}"
                )
            if "WARNING:" in result.stderr or "ERROR:" in result.stderr:
                raise RuntimeError(f"OpenSCAD reported diagnostics for {name}: {result.stderr[-5000:]}")
        results.append({
            "file": str(target),
            "variant": name,
            "upstream_source": str(script.relative_to(ROOT)),
            "parameters": parameters,
            "command": cmd,
            "generated": not dry_run,
            "physical_fit_verified": False,
        })
    return results

def main():
    p=argparse.ArgumentParser(description="Generate native openGrid snap and openConnect receiver")
    p.add_argument("--variant", choices=["all","lite","full"], default="all")
    p.add_argument("--out", default=None)
    p.add_argument("--openscad", default="openscad")
    p.add_argument("--dry-run", action="store_true")
    a=p.parse_args()
    entries=build(variant=a.variant,output=a.out,openscad=a.openscad,dry_run=a.dry_run)
    if not a.dry_run:
        out=Path(a.out) if a.out else ROOT/"output"/"interfaces"
        (out/"manifest.json").write_text(json.dumps(entries,indent=2)+"\n",encoding="utf-8")
    for e in entries:
        print(f"{'PLAN' if a.dry_run else 'BUILT'}: {e['file']}")

if __name__=="__main__":
    main()
