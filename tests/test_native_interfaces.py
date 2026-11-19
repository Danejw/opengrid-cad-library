"""Test source provenance and generator contracts without running OpenSCAD."""
import hashlib
import json
import pytest
import trimesh
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"cad"/"opengrid"))
from generate_interfaces import profile_commands

UPSTREAM={
    "lib/opengrid_base.scad":"1126278b35bcf5b33ae9f264750c4e7ff7d31b47",
    "lib/opengrid_threads_lib.scad":"7b3d67cc32955f2b869b2936243ba3e8be7b4e83",
    "lib/opengrid_snap_lib.scad":"edd22ad4d40f13f665999b08e0cdc03b8ccd02af",
    "lib/openconnect_lib.scad":"50642b9307c7806c7718531406af524f5186c06b",
    "opengrid_parametric_snap.scad":"085af70151413ac042d39ddccd0b45af92a145ee",
    "openconnect_plate.scad":"49d0819f687cbb4b8bab79cd1b8eb14a829f1485",
}

def git_blob_sha(path:Path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def test_native_source_files_are_unmodified():
    for filename,expected in UPSTREAM.items():
        p=ROOT/"vendor"/"mitufy-opengrid"/filename
        assert p.exists(),filename
        assert git_blob_sha(p)==expected,filename

def test_full_lite_and_receiver_are_present():
    configs=profile_commands("all")
    assert len(configs)==3
    profiles={filename:params for filename,_,params in configs}
    assert profiles["opengrid_openconnect_snap_lite.stl"]["snap_thickness"]==4.0
    assert profiles["opengrid_openconnect_snap_full.stl"]["snap_thickness"]==6.8
    assert profiles["opengrid_openconnect_receiver_2x1.stl"]["plate_horizontal_size"]==70
    assert profiles["opengrid_openconnect_receiver_2x1.stl"]["plate_vertical_size"]==42

def test_interfaces_unverified_until_physical_test():
    x=json.loads((ROOT/"config"/"interfaces.json").read_text())
    assert x["grid_pitch_mm"]==28
    for entry in x["components"]:
        assert entry["fit_verified"] is False
        assert entry["load_tested"] is False

def test_native_mesh_to_3mf_preserves_dimensions(tmp_path):
    from native_mesh import convert_native_stl_to_3mf
    source=tmp_path/"sample.stl"
    dest=tmp_path/"sample.3mf"
    trimesh.creation.box(extents=[28,28,4]).export(source)
    data=convert_native_stl_to_3mf(source,dest)
    assert data["topology_preserved"] is True
    assert data["physical_fit_verified"] is False
    model=trimesh.load_mesh(dest)
    assert model.is_watertight and model.is_volume

def test_no_disconnected_real_geometry_is_discarded(tmp_path):
    from native_mesh import convert_native_stl_to_3mf
    import numpy as np
    from trimesh.util import concatenate
    a=trimesh.creation.box(extents=[28,28,4])
    b=trimesh.creation.box(extents=[3,3,3])
    b.apply_translation([40,0,0])
    original=concatenate([a,b])
    src=tmp_path/"two.stl"
    original.export(src)
    with pytest.raises(ValueError):
        convert_native_stl_to_3mf(src,tmp_path/"two.3mf")
