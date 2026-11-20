"""Original board provenance and publisher asset integrity tests."""
import hashlib
import json
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_official_boards import validate_and_stage

def test_official_downloads_are_exact_source_files():
    data = json.loads((ROOT / "vendor/davidd-opengrid/manifest.json").read_text())
    assert data["publisher"] == "David D (@DavidD)"
    assert data["license"] == "CC BY 4.0"
    assert len(data["boards"]) == 4
    assert len(data["files"]) == 7
    for entry in data["files"]:
        raw = (ROOT / entry["path"]).read_bytes()
        assert len(raw) == entry["size"]
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"]
        assert entry["url"].startswith("https://files.printables.com/media/prints/1214361/")
    for board in data["boards"]:
        assert board["cells"] in {2,4}
        assert board["variant"] in {"Lite","Full"}

def test_original_boards_validate_and_stage(tmp_path):
    # Run actual mesh checks against the checked-in upstream originals.
    # Stage in a disposable directory with links to avoid touching output/.
    (tmp_path / "vendor").mkdir()
    import shutil
    shutil.copytree(ROOT / "vendor/davidd-opengrid", tmp_path / "vendor/davidd-opengrid")
    records = validate_and_stage(tmp_path)
    assert len(records) == 4
    for r in records:
        assert r["faces"] > 40
