"""Web catalog should always reflect real CAD output and preserve test statuses."""
import importlib.util
import json
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'scripts' / 'build_site_assets.py'
spec = importlib.util.spec_from_file_location('opengrid_asset_builder', MOD)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_eight_source_models_and_unique_ids():
    assert len(module.MODELS) == 8
    assert len({m['id'] for m in module.MODELS}) == 8
    assert all(m['file'].endswith(('.stl', '.3mf')) for m in module.MODELS)


def test_all_mating_interfaces_remain_unverified():
    assert {'og-oc-snap-lite-v1', 'og-oc-snap-full-v1', 'og-oc-receiver-2x1-v1'} <= {m['id'] for m in module.MODELS}
    assert all('fitVerified' not in m for m in module.MODELS)


def test_missing_verified_report_is_an_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        module.export_assets(tmp_path, tmp_path / 'assets')
