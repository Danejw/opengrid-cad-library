#!/usr/bin/env python3
"""Convert verified openGrid CAD pipeline outputs into a static, versioned web catalog.

No generated geometry is invented in the browser. The GLB meshes here come from
validated generated STL/3MF files. STEP/3MF/STL originals remain downloadable.
"""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any
import trimesh
import numpy as np
import math

ROOT = Path(__file__).resolve().parents[1]
MODELS = [
    dict(id='og-official-full-4x4', name='Official Full board 4×4', type='Boards', tagline='David D original board, 4×4 cells', file='official/openGrid 4x4.3mf', preview='openGrid 4x4.png', description='Unmodified publisher-authored openGrid Full board, 4×4 cells, for genuine printable mounting geometry.', interface='openGrid Full board · original publisher geometry', material='Publisher original', tags=['Official', 'Board', 'Full', '4×4'], source='vendor/davidd-opengrid/boards/openGrid 4x4.3mf', sourceUrl='https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem/files', editable='Original 3MF', accent='#c6ccaa'),
    dict(id='og-official-lite-4x4', name='Official Lite board 4×4', type='Boards', tagline='David D original Lite board, 4×4 cells', file='official/openGrid Lite 4x4.3mf', preview='openGrid Lite 4x4.png', description='Unmodified publisher-authored openGrid Lite board, 4×4 cells, with its genuine mounting geometry.', interface='openGrid Lite board · original publisher geometry', material='Publisher original', tags=['Official', 'Board', 'Lite', '4×4'], source='vendor/davidd-opengrid/boards/openGrid Lite 4x4.3mf', sourceUrl='https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem/files', editable='Original 3MF + STEP', accent='#b3cce4'),
    dict(id='og-official-full-2x2', name='Official Full board 2×2', type='Boards', tagline='David D original board, 2×2 cells', file='official/openGrid 2x2.3mf', preview='openGrid 2x2.png', description='Unmodified publisher-authored openGrid Full board, 2×2 cells, useful for small snap and print tests.', interface='openGrid Full board · original publisher geometry', material='Publisher original', tags=['Official', 'Board', 'Full', '2×2'], source='vendor/davidd-opengrid/boards/openGrid 2x2.3mf', sourceUrl='https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem/files', editable='Original 3MF + STEP', accent='#bcd2ba'),
    dict(id='og-official-lite-2x2', name='Official Lite board 2×2', type='Boards', tagline='David D original Lite board, 2×2 cells', file='official/openGrid Lite 2x2.3mf', preview='openGrid Lite 2x2.png', description='Unmodified publisher-authored openGrid Lite board, 2×2 cells, useful for test installations.', interface='openGrid Lite board · original publisher geometry', material='Publisher original', tags=['Official', 'Board', 'Lite', '2×2'], source='vendor/davidd-opengrid/boards/openGrid Lite 2x2.3mf', sourceUrl='https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem/files', editable='Original 3MF + STEP', accent='#cbc6e7'),
    dict(id='og-cable-hook-v1', name='Cable hook', type='Accessories', tagline='A lightweight modular cable organizer', file='accessories/opengrid_openconnect_cable_hook.3mf', preview='opengrid_openconnect_cable_hook.png', description='A cable-management prototype attached to a native two-cell openConnect receiving plate.', interface='Native openConnect receiver', material='PETG candidate', tags=['Cable management','OpenConnect','2-cell'], source='cad/opengrid/cable_hook.scad', editable='OpenSCAD source', accent='#7fe3c5', parameters={"stemLengthIn": 0.75, "stemDiameterIn": 0.30, "lipDiameterIn":0.50}),
    dict(id='og-bare-snap-lite-v1', name='Bare Lite snap', type='Connectors', tagline='Directional modeling snap, 3.4 mm Lite profile', file='interfaces/opengrid_bare_snap_lite.3mf', preview='opengrid_bare_snap_lite.png', description='Directional bare snap generated from pinned upstream geometry. Intended as a modeling foundation for Lite and compatible Full board accessories; print fit is untested.', interface='openGrid Lite · Bare directional', material='Modeling reference', tags=['Native geometry','Bare','Lite','Directional'], source='vendor/mitufy-opengrid/opengrid_parametric_snap.scad', editable='OpenSCAD source', accent='#b7c4da'),
    dict(id='og-bare-snap-full-v1', name='Bare Full snap', type='Connectors', tagline='Directional modeling snap, 6.8 mm Full profile', file='interfaces/opengrid_bare_snap_full.3mf', preview='opengrid_bare_snap_full.png', description='Directional bare snap generated from pinned upstream geometry for the Full board. Intended as a native modeling foundation; print fit is untested.', interface='openGrid Full · Bare directional', material='Modeling reference', tags=['Native geometry','Bare','Full','Directional'], source='vendor/mitufy-opengrid/opengrid_parametric_snap.scad', editable='OpenSCAD source', accent='#a4c4d0'),
    dict(id='og-oc-snap-lite-v1', name='Lite openConnect snap', type='Connectors', tagline='Directional snap with openConnect head, 4 mm profile', file='interfaces/opengrid_openconnect_snap_lite.3mf', preview='opengrid_openconnect_snap_lite.png', description='Native publisher-authored openGrid Lite thickness snap with openConnect head.', interface='openGrid Lite · openConnect', material='To be tested', tags=['Native geometry','Lite','Mounting'], source='vendor/mitufy-opengrid/opengrid_parametric_snap.scad', editable='OpenSCAD source', accent='#caa9ff'),
    dict(id='og-oc-snap-full-v1', name='Full openConnect snap', type='Connectors', tagline='Directional snap with openConnect head, 6.8 mm profile', file='interfaces/opengrid_openconnect_snap_full.3mf', preview='opengrid_openconnect_snap_full.png', description='Native publisher-authored openGrid Full thickness snap with openConnect head.', interface='openGrid Full · openConnect', material='To be tested', tags=['Native geometry','Full','Mounting'], source='vendor/mitufy-opengrid/opengrid_parametric_snap.scad', editable='OpenSCAD source', accent='#b5c7f2'),
    dict(id='og-oc-receiver-2x1-v1', name='Receiving plate', type='Connectors', tagline='Two-cell openConnect accessory interface', file='interfaces/opengrid_openconnect_receiver_2x1.3mf', preview='opengrid_openconnect_receiver_2x1.png', description='A 2×1 native openConnect slot layout on a supported mounting plate.', interface='Native openConnect 2×1', material='To be tested', tags=['Native geometry','Adapter','2-cell'], source='vendor/mitufy-opengrid/openconnect_plate.scad', editable='OpenSCAD source', accent='#edbd8c'),
    dict(id='og-tray-v1', name='Storage tray', type='Prototypes', tagline='Compact modular desk organizer', file='grid_tray.stl', preview='grid_tray.png', description='An independently printable desk tray with grid-aligned mounting positions. Native wall mounting has not been integrated.', interface='28 mm positioning only', material='PLA / PETG candidate', tags=['Storage','Standalone','Tray'], source='cad/library.py', editable='STEP + CadQuery', accent='#a6d5f5'),
    dict(id='og-crate-v1', name='Vented crate', type='Prototypes', tagline='Airflow-friendly storage container', file='vented_crate.stl', preview='vented_crate.png', description='A standalone ventilated crate with 28 mm-aligned openings. The openings are not native openGrid connection slots.', interface='Pitch-aligned openings only', material='PLA / PETG candidate', tags=['Storage','Standalone','Crate'], source='cad/library.py', editable='STEP + CadQuery', accent='#b7d7b0'),
    dict(id='og-adapter-blank-v1', name='Adapter blank', type='Prototypes', tagline='A base for future mounting systems', file='adapter_blank.stl', preview='adapter_blank.png', description='Blank plate with grid-aligned fastener positions, ready to receive a properly validated connector.', interface='Alignment only', material='PLA / PETG candidate', tags=['Template','Adapter','Mounting'], source='cad/library.py', editable='STEP + CadQuery', accent='#ebc4a3'),
    dict(id='og-pitch-calibration-v1', name='Pitch coupon', type='Prototypes', tagline='Reference geometry for print calibration', file='pitch_coupon.stl', preview='pitch_coupon.png', description='Dimensioned 28 mm pitch measurement coupon for calibrating a print. It is not a snap-compatible board.', interface='28 mm reference pitch', material='PLA / PETG candidate', tags=['Calibration','Reference','Test'], source='cad/library.py', editable='STEP + CadQuery', accent='#e7d9aa'),
]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def export_assets(output_dir: Path, target_dir: Path, revision: str = 'local') -> dict:
    output_dir, target_dir = Path(output_dir), Path(target_dir)
    report = _load_json(output_dir / 'reports' / 'engineering_report.json')
    verified = {entry['part']: entry for entry in report['records']}
    model_dir = target_dir / 'models'
    images_dir = target_dir / 'previews'
    exports_dir = target_dir / 'downloads'
    for folder in (model_dir, images_dir, exports_dir):
        folder.mkdir(parents=True, exist_ok=True)
    data = []
    for config in MODELS:
        config = dict(config)
        input_file = output_dir / config.pop('file')
        key = input_file.stem
        if key not in verified:
            raise ValueError(f'Missing verified CAD record for {key}')
        check = verified[key]
        if check.get('cad_geometry_valid') is not True or check.get('mesh_watertight') is not True:
            raise ValueError(f'Unverified mesh {key}')
        if not input_file.exists():
            raise FileNotFoundError(input_file)
        mesh = trimesh.load_mesh(input_file, process=True)
        if not isinstance(mesh, trimesh.Trimesh) or not mesh.is_watertight or not mesh.is_volume or mesh.volume <= 0:
            raise ValueError(f'Invalid source mesh {input_file}')
        # Explicitly preserve source geometry coordinates in millimetres.
        glb_path = model_dir / f'{config["id"]}.glb'
        mesh.export(glb_path)
        if not glb_path.is_file() or glb_path.stat().st_size < 256:
            raise ValueError(f'GLB export failed for {input_file}')
        # Verify published viewer geometry preserves the source CAD mesh.
        exported = trimesh.load(glb_path, force='mesh', process=True)
        if (not isinstance(exported, trimesh.Trimesh)
                or len(exported.faces) != len(mesh.faces)
                or not np.allclose(exported.bounds, mesh.bounds, rtol=0, atol=0.001)
                or not math.isclose(exported.volume, mesh.volume, rel_tol=0.0001, abs_tol=0.001)):
            raise ValueError(f'Web GLB changed source CAD geometry: {input_file}')
        preview_src = output_dir / 'previews' / config.pop('preview')
        if not preview_src.is_file():
            raise FileNotFoundError(preview_src)
        preview_dest = images_dir / f'{config["id"]}.png'
        shutil.copyfile(preview_src, preview_dest)
        formats = {input_file.suffix[1:].upper(): f'downloads/{input_file.name}'}
        shutil.copyfile(input_file, exports_dir / input_file.name)
        step = input_file.with_suffix('.step') if config['type'] == 'Boards' else output_dir / (input_file.stem + '.step')
        if step.is_file():
            shutil.copyfile(step, exports_dir / step.name)
            formats['STEP'] = f'downloads/{step.name}'
        config['model'] = f'models/{config["id"]}.glb'
        config['preview'] = f'previews/{config["id"]}.png'
        config['downloads'] = formats
        config['boundsInches'] = check['bounds_inches']
        config['triangles'] = check['triangles']
        config['volumeCubicInches'] = check['volume_cubic_inches']
        config['validation'] = {
            'cadValid': True,
            'meshWatertight': True,
            'slicerVerified': False,
            'fitVerified': False,
            'loadTested': False,
        }
        config['provenance'] = ('David D original publisher file (CC BY 4.0)' if config['type'] == 'Boards'
                               else 'Pinned mitufy upstream generator (CC BY 4.0)' if config['type'] == 'Connectors'
                               else 'Native receiver, custom accessory' if config['type'] == 'Accessories'
                               else 'Original CadQuery prototype')
        data.append(config)
    catalog = {
        'schemaVersion': '1.0.0',
        'generatedFrom': revision,
        'unit': 'in',
        'verification': 'CAD software checks only; physical fit and load unverified',
        'models': data,
    }
    (target_dir / 'catalog.json').write_text(json.dumps(catalog, indent=2) + '\n', encoding='utf-8')
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description='Publish verified CAD geometry as static web assets')
    parser.add_argument('--output', default=str(ROOT / 'output'))
    parser.add_argument('--dest', default=str(ROOT / 'web' / 'public' / 'assets'))
    parser.add_argument('--revision', default='local')
    args = parser.parse_args()
    result = export_assets(Path(args.output), Path(args.dest), args.revision)
    print(f'Prepared {len(result["models"])} verified GLB models, previews, and source downloads')


if __name__ == '__main__':
    main()
