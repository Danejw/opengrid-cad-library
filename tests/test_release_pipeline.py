"""No printer required for Phase 3 release-report tests."""
from pathlib import Path
import sys
import trimesh
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"cad"/"opengrid"))
from release_pipeline import EXPECTED,inspect

def test_expected_parts_cover_native_interface_and_accessory():
    assert "openGrid 2x2.3mf" in EXPECTED
    assert "openGrid Lite 2x2.3mf" in EXPECTED
    assert "openGrid 4x4.3mf" in EXPECTED
    assert "openGrid Lite 4x4.3mf" in EXPECTED
    assert "opengrid_bare_snap_full.3mf" in EXPECTED
    assert "opengrid_bare_snap_lite.3mf" in EXPECTED
    assert "opengrid_openconnect_snap_full.3mf" in EXPECTED
    assert "opengrid_openconnect_snap_lite.3mf" in EXPECTED
    assert "opengrid_openconnect_cable_hook.3mf" in EXPECTED

def test_engineering_record_never_claims_physical_fit(tmp_path):
    sample=tmp_path/"sample.stl"
    trimesh.creation.box(extents=[28,28,4]).export(sample)
    info=inspect(sample)
    assert info["mesh_watertight"]
    assert info["slicer_verified"] is False
    assert info["physical_fit_verified"] is False
    assert info["load_tested"] is False
    assert info["filament_used_lbs"] is None
    assert info["bounds_inches"][0]==pytest.approx(28/25.4,abs=0.001)

def test_nonmanifold_mesh_rejected(tmp_path):
    sample=tmp_path/"triangle.stl"
    mesh=trimesh.Trimesh(vertices=[[0,0,0],[1,0,0],[0,1,0]],faces=[[0,1,2]],process=False)
    mesh.export(sample)
    with pytest.raises(ValueError):
        inspect(sample)
