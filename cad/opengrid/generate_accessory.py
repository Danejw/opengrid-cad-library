"""Phase 2: create a useful accessory from the native Phase 1 receiver."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"cad"/"opengrid"/"cable_hook.scad"

def build(*, receiver=None, output=None, stem_length_in=0.75,
          stem_diameter_in=0.30, lip_diameter_in=0.50, openscad="openscad"):
    if not 0.3<=stem_length_in<=2.0:
        raise ValueError("stem length must be 0.3..2.0 inches")
    if not 0.18<=stem_diameter_in<=0.5:
        raise ValueError("stem diameter must be 0.18..0.5 inches")
    if lip_diameter_in<=stem_diameter_in or lip_diameter_in>0.75:
        raise ValueError("lip diameter must be greater than stem and at most 0.75 inches")
    native=Path(receiver) if receiver else ROOT/"output"/"interfaces"/"opengrid_openconnect_receiver_2x1.stl"
    if not native.is_file():
        raise FileNotFoundError(
            f"Native upstream receiver missing: {native}. "
            "Run python cad/opengrid/generate_interfaces.py first."
        )
    dest=Path(output) if output else ROOT/"output"/"accessories"
    dest.mkdir(parents=True,exist_ok=True)
    target=dest/"opengrid_openconnect_cable_hook.stl"
    parameters={
      "receiver_file":str(native.resolve()),
      "stem_length_mm":round(stem_length_in*25.4,5),
      "stem_diameter_mm":round(stem_diameter_in*25.4,5),
      "lip_diameter_mm":round(lip_diameter_in*25.4,5),
    }
    cmd=[openscad,"-o",str(target.resolve())]
    for k,v in parameters.items():
        cmd+=["-D",f"{k}={json.dumps(v)}"]
    cmd.append(str(SOURCE))
    run=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,check=False)
    if run.returncode or not target.is_file() or target.stat().st_size<100:
        raise RuntimeError(f"OpenSCAD cable hook generation failed: {run.stderr[-4500:]}")
    if "ERROR:" in run.stderr or "WARNING:" in run.stderr:
        raise RuntimeError(f"OpenSCAD cable hook warnings: {run.stderr[-4500:]}")
    metadata={
      "id":"og-cable-hook-v1",
      "source":"cad/opengrid/cable_hook.scad",
      "native_connector_source":"vendor/mitufy-opengrid/openconnect_plate.scad",
      "connector":"openConnect 2x1 receiver, authentic upstream geometry",
      "parameters":{k:v for k,v in parameters.items() if k!="receiver_file"},
      "output":str(target),
      "source_editable":True,
      "step_available":False,
      "cad_valid":False,
      "slicer_verified":False,
      "fit_verified":False,
      "load_tested":False,
      "notes":"Light-duty cable organizer; solid and mesh checks pending, actual fit untested"
    }
    (dest/"cable_hook_manifest.json").write_text(json.dumps(metadata,indent=2)+"\n")
    return target

def main():
    p=argparse.ArgumentParser(description="Build source-driven openGrid cable hook using native openConnect receiver")
    p.add_argument("--receiver")
    p.add_argument("--out")
    p.add_argument("--stem-length-in",type=float,default=0.75)
    p.add_argument("--stem-diameter-in",type=float,default=0.30)
    p.add_argument("--lip-diameter-in",type=float,default=0.50)
    p.add_argument("--openscad",default="openscad")
    a=p.parse_args()
    f=build(receiver=a.receiver,output=a.out,stem_length_in=a.stem_length_in,
            stem_diameter_in=a.stem_diameter_in,lip_diameter_in=a.lip_diameter_in,openscad=a.openscad)
    print(f"BUILT: {f}")

if __name__=="__main__":main()
