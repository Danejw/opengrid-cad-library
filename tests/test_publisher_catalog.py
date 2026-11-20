"""Publisher file index and sample geometry verification."""
from __future__ import annotations
import json
import shutil
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from prepare_publisher_samples import stage
INDEX=ROOT/"vendor/opengrid-sources/published-cad-index.json"

def test_full_original_file_index():
    index=json.loads(INDEX.read_text())
    assert len(index["sources"])==13
    assert len(index["models"])==362
    assert index["totalFiles"]==679
    assert sum(len(m["files"]) for m in index["models"])==679
    assert all(m["sourceId"] in {s["id"] for s in index["sources"]} for m in index["models"])
    assert any(s["license"]=="CC BY-NC-SA 4.0" for s in index["sources"])
    assert any(s["creator"]=="mitufy" for s in index["sources"])
    assert all(f["id"] and f["bytes"]>0 for m in index["models"] for f in m["files"])
def test_exact_publisher_source_samples(tmp_path):
    target=tmp_path/"vendor/opengrid-sources"
    target.mkdir(parents=True)
    shutil.copy(ROOT/"vendor/opengrid-sources/imported-manifest.json",target)
    shutil.copytree(ROOT/"vendor/opengrid-sources/originals",target/"originals")
    records=stage(tmp_path)
    assert len(records)==8
    assert all(x["faces"]>20 for x in records)
