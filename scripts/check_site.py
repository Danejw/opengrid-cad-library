#!/usr/bin/env python3
"""Deterministic smoke check of the deployed static site and published CAD assets."""
import argparse
import json
from pathlib import Path
import struct


def validate(dist: Path) -> None:
    index = dist / 'index.html'
    assert index.is_file() and index.stat().st_size > 200
    html = index.read_text(encoding='utf-8')
    assert '/opengrid-cad-library/' in html, 'Vite base path must support GitHub Pages project site'
    assert '<div id="root"></div>' in html
    assets = dist / 'assets'
    catalog = json.loads((assets / 'catalog.json').read_text(encoding='utf-8'))
    models = catalog['models']
    assert len(models) == 20, f'Expected six official accessories plus fourteen existing CAD designs, got {len(models)}'
    assert all('STEP' in m['downloads'] for m in models if m['id'].startswith('og-official-') and m['type'] != 'Boards')
    assert sum(m['type'] == 'Boards' for m in models) == 4
    assert all('David D' in m['provenance'] for m in models if m['type'] == 'Boards')
    assert 'STEP' in next(m for m in models if m['id'] == 'og-official-full-2x2')['downloads']
    assert 'STEP' in next(m for m in models if m['id'] == 'og-official-lite-2x2')['downloads']
    assert 'STEP' in next(m for m in models if m['id'] == 'og-official-lite-4x4')['downloads']
    by_id = {m['id']: m for m in models}
    assert {'og-bare-snap-lite-v1', 'og-bare-snap-full-v1'} <= set(by_id)
    assert 'Bare' in by_id['og-bare-snap-full-v1']['name']
    assert 'Bare' in by_id['og-bare-snap-lite-v1']['name']
    assert 'openConnect' in by_id['og-oc-snap-full-v1']['name']
    assert 'openConnect' in by_id['og-oc-snap-lite-v1']['name']
    assert len(set(m['id'] for m in models)) == len(models)
    for model in models:
        assert model['validation']['cadValid'] is True
        assert model['validation']['meshWatertight'] is True
        for flag in ['slicerVerified', 'fitVerified', 'loadTested']:
            assert model['validation'][flag] is False, (model['id'], flag)
        for key in ('model', 'preview'):
            f = assets / model[key]
            assert f.is_file() and f.stat().st_size > 400, f
        for _, path in model['downloads'].items():
            assert (assets / path).is_file(), path
        with (assets / model['model']).open('rb') as stream:
            assert stream.read(4) == b'glTF', model['id']
        with (assets / model['preview']).open('rb') as stream:
            assert stream.read(8) == b'\x89PNG\r\n\x1a\n', model['id']
        assert len(model['boundsInches']) == 3
        assert all(0 < float(x) < 20 for x in model['boundsInches'])
    jsfiles = list((dist / 'assets').glob('*.js'))
    assert jsfiles, 'No compiled JavaScript bundle'
    assert (dist / '.nojekyll').is_file(), 'Pages must bypass Jekyll'
    print(f'PASS: {len(models)} actual GLB previews and downloads, validated HTML and JS, base path correct')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dist', default='web/dist')
    validate(Path(p.parse_args().dist))
