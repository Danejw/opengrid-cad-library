"""Publisher accessory integrity must remain deterministic and byte-accurate."""
import hashlib
import json
import shutil
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_official_accessories import validate_and_stage

def test_publisher_file_integrity_and_licenses():
    manifest = json.loads((ROOT / "vendor/davidd-opengrid/accessories-manifest.json").read_text())
    assert manifest["publisher"] == "David D (@DavidD)"
    assert manifest["license"] == "CC BY 4.0"
    assert len(manifest["models"]) == 6
    assert len(manifest["files"]) == 12
    for item in manifest["files"]:
        data = (ROOT / item["path"]).read_bytes()
        assert len(data) == item["size"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        assert item["printables_file_id"]
        assert item["url"].startswith("https://files.printables.com/")
    assert len({m["id"] for m in manifest["models"]}) == 6

def test_original_accessory_geometry(tmp_path):
    (tmp_path / "vendor").mkdir()
    shutil.copytree(ROOT / "vendor/davidd-opengrid",tmp_path / "vendor/davidd-opengrid")
    result = validate_and_stage(tmp_path)
    assert len(result) == 6
    assert all(r["faces"] > 20 for r in result)
