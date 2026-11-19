# Utility Scripts Reference

This skill includes Python scripts in the `scripts/` directory. **Copy them next to your model script** before running (they must be importable from the same directory).

## Overview

| Script | Purpose |
|--------|---------|
| `run_cadquery_model.py` | Subprocess wrapper: runs a CadQuery script, renders preview, emits JSON result for self-correction loops |
| `preview.py` | Headless STL → multi-view PNG renderer (6 views with dimensions footer) |
| `mesh_io.py` | STL loading with validation (no pyrender dep). Used by wrapper and converter |
| `gridfinity.py` | Spec-compatible Gridfinity bin generator module |
| `outline_from_scan.py` | Extracts 2D pocket outline from a 3D scan for `add_polygon_pocket` |
| `stl_to_3mf.py` | STL → 3MF converter for Bambu Studio / PrusaSlicer |

## run_cadquery_model.py

```bash
python3 run_cadquery_model.py path/to/model.py                    # basic run
python3 run_cadquery_model.py path/to/model.py --preview          # run + render
python3 run_cadquery_model.py path/to/model.py --preview --strict # fail on non-watertight
python3 run_cadquery_model.py model.py --views iso --timeout 300  # single view, 5min timeout
```

**JSON output keys:** `success`, `script`, `stls`, `stl`, `previews`, `preview`, `threemfs`, `threemf`, `steps`, `step`, `watertight`, `stdout`, `stderr`, `returncode`

**Exit codes:** 0 success, 1 script/preview/strict failure, 2 interpreter not launchable, 3 timeout

Discovers STL, 3MF, and STEP files produced during execution. With `--strict`, absence of STL output is a hard failure.

## preview.py

```bash
python3 preview.py model.stl preview.png --views multi    # 6-view (default)
python3 preview.py model.stl preview.png --views iso      # single isometric
python3 preview.py model.stl --resolution 800             # higher-res per view
python3 preview.py model.stl --strict                     # fail on non-watertight
python3 preview.py model.stl --title "My Part" --subtitle "v2.1"
```

On Linux, automatically sets `PYOPENGL_PLATFORM=egl` for headless GPU rendering.

**6-view layout:** isometric, front, right (top row), back-iso, top, bottom (bottom row). Footer shows bounding box, volume, triangle count, watertight status, and PLA weight estimate.

## mesh_io.py

```python
from mesh_io import load_mesh

tm = load_mesh("model.stl")
# Raises ValueError on: invalid/empty mesh, zero faces, NaN vertices
# Automatically removes degenerate triangles and merges vertices
```

## stl_to_3mf.py

```bash
python3 stl_to_3mf.py model.stl              # → model.3mf
python3 stl_to_3mf.py a.stl b.stl c.stl      # multi-file
python3 stl_to_3mf.py --out other.3mf model.stl
```

**WARNING:** trimesh's 3MF writer mangles internal cavities. For CadQuery parts with `cut()` cavities (magnet pockets, enclosed voids), export 3MF directly from CadQuery:
```python
cq.exporters.export(result, "name.3mf")
```

## outline_from_scan.py

Extracts the max cross-section outline from a 3D scan. Pipeline: PCA-align → scale to real dims → slice every mm → union sections → simplify.

```bash
python3 outline_from_scan.py scan.stl --dims 124.9x84.3x51 --zmax 19 --out outline.json
python3 outline_from_scan.py scan.stl --dims 124.9x84.3x51 --zmax 19 --rotate-min-square
```

**Options:**
- `--dims LxWxH`: real dimensions in mm (omit to trust scan scale)
- `--zmax`: pocket depth — outline covers Z 0..zmax mm (required)
- `--step`: slice spacing (default 1.0mm)
- `--simplify`: simplification tolerance (default 0.25mm)
- `--rotate-min-square`: rotate outline to minimize bounding square
- `--clearance`: pocket clearance for rotation search (default 1.3mm)
- `--out`: write JSON point list (default: stdout)

Output is a list of `[x, y]` points ready for `GridfinityBin.add_polygon_pocket(points)`.

## gridfinity.py

See `references/gridfinity.md` for the full API reference.
