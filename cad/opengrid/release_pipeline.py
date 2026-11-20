"""Phase 3: repeatable preview and evidence manifest for CAD outputs.

Runs only after the native interface and accessory exporters in CI.
Never treats a CAD mesh as physical fit or printer load testing.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import trimesh

ROOT=Path(__file__).resolve().parents[2]
EXPECTED={
    "pitch_coupon.stl","grid_tray.stl","vented_crate.stl","adapter_blank.stl",
    "openGrid 2x2.3mf", "openGrid Lite 2x2.3mf",
    "openGrid 4x4.3mf", "openGrid Lite 4x4.3mf",
    "openGrid Minimal Hook.3mf",
    "openGrid Wall Mount.3mf",
    "openGrid Lite Wall Mount.3mf",
    "openGrid Color_Cover Snap.3mf",
    "openGrid Multiconnect Directional Snap v2.3mf",
    "openGrid M3 Nut Snap.3mf",
    "opengrid_bare_snap_lite.3mf",
    "opengrid_bare_snap_full.3mf",
    "opengrid_openconnect_snap_lite.3mf",
    "opengrid_openconnect_snap_full.3mf",
    "opengrid_openconnect_receiver_2x1.3mf",
    "opengrid_openconnect_cable_hook.3mf",
    "openGrid Bare Directional Snap v2.1.3mf",
    "openGrid Bare Directional Lite Snap v2.3mf",
    "Connector Insert Tool.3mf",
    "openGrid M4 Nut Snap.3mf",
    "openGrid HSW Snap.3mf",
    "openGrid Underware 2x Channel.3mf",
    "openGrid Gridfinity Shelve 2x1.3mf",
    "openGrid Multiboard Tile Snap.3mf"
}

def inspect(path: Path):
    m=trimesh.load_mesh(path,process=True)
    if isinstance(m,trimesh.Scene):
        m=m.to_geometry()
    if not isinstance(m,trimesh.Trimesh):
        raise ValueError(f"Not a mesh: {path}")
    if len(m.vertices)<4 or len(m.faces)<4 or not m.is_watertight or not m.is_volume or m.volume<=0:
        raise ValueError(f"Invalid, non-manifold, or zero-volume mesh: {path}")
    bounds=[float(x) for x in m.extents]
    if any(x<=0 or x>=300 for x in bounds):
        raise ValueError(f"Unexpected part dimensions: {path} {bounds}")
    return {
       "part":path.stem,
       "source_file":str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
       "bounds_inches":[round(x/25.4,3) for x in bounds],
       "mesh_watertight":True,
       "cad_geometry_valid":True,
       "mesh_connected_components":len(m.split(only_watertight=False)),
       "triangles":len(m.faces),
       "volume_cubic_inches":round(float(m.volume)/25.4**3,5),
       "filament_used_lbs":None,
       "print_time":None,
       "slicer_verified":False,
       "physical_fit_verified":False,
       "load_tested":False,
    }

def preview(stl: Path, destination: Path, openscad: str, xvfb: str):
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        scene=Path(tmp)/"scene.scad"
        scene.write_text("import("+json.dumps(str(stl.resolve()))+", convexity=10);\n",encoding="utf-8")
        command=[xvfb,"-a",openscad,"--autocenter","--viewall",
                 "--imgsize=720,540","--colorscheme=Metallic",
                 "-o",str(destination.resolve()),str(scene)]
        run=subprocess.run(command,capture_output=True,text=True,timeout=180)
        if run.returncode or not destination.exists() or destination.stat().st_size<1000:
            raise RuntimeError(f"Preview render failed for {stl}: {run.stderr[-2000:]}")
        with destination.open("rb") as stream:
            if stream.read(8)!=bytes([137,80,78,71,13,10,26,10]):
                raise RuntimeError(f"Expected PNG: {destination}")
    return destination

def build(root=ROOT, openscad="openscad", xvfb="xvfb-run", make_previews=True):
    root=Path(root)
    output=root/"output"
    stls=sorted(output.rglob("*.stl")) + sorted(output.rglob("*.3mf"))
    found={p.name for p in stls}
    missing=EXPECTED-found
    if missing:
        raise ValueError(f"Required CAD exports absent: {sorted(missing)}")
    reports=[]
    for stl in stls:
        info=inspect(stl)
        if make_previews:
            png=output/"previews"/(stl.stem+".png")
            preview(stl,png,openscad,xvfb)
            info["preview"]=str(png.relative_to(root))
        reports.append(info)
    report={
       "report_format":"openGrid-engineering-preflight-v1",
       "unit_system":"inches and pounds (machine source models use mm)",
       "status":"CAD_GEOMETRY_ONLY_PHYSICAL_TESTS_PENDING",
       "records":reports,
       "limitations":[
          "Software CAD and mesh checks cannot verify native snap retention.",
          "Print time, filament mass, supports and slicer fit require a real slicer profile.",
          "Mechanical strength and wear require an actual print and testing."
       ]
    }
    dest=output/"reports"
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"engineering_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    summary=["# Automated engineering preflight", "",
      f"CAD meshes validated: {len(reports)}", "",
      "All physical-fit and load claims: **unverified**", "",
      "No printer has been commanded to print.", "",
      "Generated from the source-controlled repository by GitHub Actions.", ""]
    for record in reports:
        summary.append(f"- **{record['part']}**: {' x '.join(map(str,record['bounds_inches']))} in, watertight. Preview: {record.get('preview','not generated')}")
    (dest/"README.md").write_text("\n".join(summary)+"\n",encoding="utf-8")
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--no-preview",action="store_true")
    parser.add_argument("--openscad",default="openscad")
    parser.add_argument("--xvfb",default="xvfb-run")
    args=parser.parse_args()
    report=build(make_previews=not args.no_preview,openscad=args.openscad,xvfb=args.xvfb)
    print(f"Preflight: {len(report['records'])} watertight source-generated meshes; see output/reports/")

if __name__=="__main__":main()
