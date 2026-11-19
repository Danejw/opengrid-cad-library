"""Static Phase 2 design assertions, no printing hardware needed."""
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"cad"/"opengrid"))
from generate_accessory import build

def test_customization_requires_usable_dimensions(tmp_path):
    with pytest.raises(ValueError):
        build(output=tmp_path,stem_length_in=0)
    with pytest.raises(ValueError):
        build(output=tmp_path,lip_diameter_in=0.2)

def test_cannot_fake_missing_native_receiver(tmp_path):
    with pytest.raises(FileNotFoundError):
        build(receiver=tmp_path/"not-an-upstream-connector.stl",output=tmp_path)

def test_source_imports_original_receiver():
    source=(ROOT/"cad"/"opengrid"/"cable_hook.scad").read_text()
    assert "import(receiver_file" in source
    assert "union()" in source
    assert "cylinder(" in source
