---
name: parametric-3d-printing
description: "Use this skill when the user wants to design a 3D-printable physical object they intend to manufacture. Triggers: any mention of '3D print', 'STL', 'parametric model', 'Gridfinity', 'enclosure', 'bracket', 'mount', 'case', 'housing', 'CadQuery', 'OpenSCAD', or a specific FDM printer (Bambu Lab, Prusa, Ender); questions about print-friendly design, snap-fits, tolerances, or wall thickness; and requests for functional parts like Arduino enclosures, cable organizers, wall mounts, adapters, or mechanical components. Also fires when the user describes a real physical object to make, provided the goal is to manufacture it. Do NOT use for: 3D rendering, animation, game assets, digital-only art, photogrammetry, sculpting, editing an existing STL file the user already has, or any 3D work that is not heading toward a printer."
---

# Parametric 3D Printing with CadQuery

## Overview

This skill generates parametric 3D models using **CadQuery** (Python) and exports STL files ready for slicing. CadQuery uses the OpenCASCADE BRep kernel — think in terms of faces/edges/topology, not CSG booleans.

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install cadquery>=2.6.1 trimesh>=4.0 pyrender>=0.1.45 Pillow>=10 numpy>=1.24 lxml>=4.9
```

Requires Python 3.10-3.12 (OCC kernel lacks 3.13+ wheels). If pip install fails, use `conda install -c cadquery -c conda-forge cadquery`.

## Core Workflow

1. **Gather requirements** — what is it, critical dimensions, mounting, printer/material
2. **Research dimensions** — web search for real-world specs; add 0.3-0.5mm clearance
3. **Phase 1**: Base shape → preview → user feedback
4. **Phase 2**: Features (holes, cutouts, bosses) → preview → user feedback
5. **Phase 3**: Fillets, final STL + preview + print recommendations
6. **Offer parameter tweaks** via summary table

This is collaborative — show progress at each phase. Do NOT deliver a finished model without intermediate feedback.

> 📖 Full phase details: `references/preview-workflow.md`

## Requirements Gathering

Ask conversationally, most important first:
- **What is it?** — object type, purpose, what it holds/protects
- **Critical dimensions** — must-fit measurements (non-negotiable)
- **Mounting** — screws, snap-fit, adhesive, magnets, freestanding?
- **Printer & material** — defaults: 0.4mm nozzle, PLA, 0.2mm layers
- **Functional needs** — ventilation, cable routing, water resistance (only if relevant)

## Script Template

```python
import cadquery as cq

# ============================================================
# PARAMETERS
# ============================================================
width = 60.0        # mm - outer width
depth = 40.0        # mm - outer depth
height = 25.0       # mm - outer height
wall = 2.0          # mm - wall thickness (min 1.2 for FDM)
corner_r = 2.0      # mm - corner fillet radius
fit_clearance = 0.3 # mm - clearance for press-fit

# ============================================================
# MODEL
# ============================================================
result = (
    cq.Workplane("XY")
    .box(width, depth, height, centered=(True, True, False))
)

# ============================================================
# EXPORT
# ============================================================
cq.exporters.export(result, "output.stl",
                    tolerance=0.01, angularTolerance=0.1)
print(f"Exported: {width}x{depth}x{height}mm")
```

## Essential Rules

- **Parameters first** — ALL dimensions in PARAMETERS section, descriptive names, units in comments
- **Bottom at Z=0** — use `centered=(True, True, False)` on `.box()`
- **Wall >= 1.2mm**, recommended 2.0mm. Clearance 0.3mm for fits.
- **Fillet before cut** — apply fillets while geometry is clean, largest radius first
- **Prefer boolean subtraction over `.shell()`** for hollowing — `.shell()` is fragile
- **Overhang < 45°** — design around supports; use chamfers on bottom edges (not fillets)
- **BRep, not CSG** — use `.faces(">Z").workplane().extrude()` instead of `.union()`

> 📖 Full rules & pitfalls: `references/print-rules.md`
> 📖 CadQuery selectors, patterns, Free Function API: `references/cadquery-advanced.md`

## Export

```python
cq.exporters.export(result, "model.stl", tolerance=0.01, angularTolerance=0.1)  # for slicing
cq.exporters.export(result, "model.step")  # optional, for CAD editing
```

Multi-part: export each part to a separate, descriptively-named STL file.

## Preview Loop

```bash
python3 run_cadquery_model.py model.py --preview --strict
```

Emits JSON with `success`, `stl`, `preview`, `watertight`, `stderr`. If failed, fix and re-run. Always self-review the preview before showing the user.

> 📖 Full preview workflow: `references/preview-workflow.md`
> 📖 Design review checklist: `references/design-review.md`

## Gridfinity

For Gridfinity bins, use the bundled `gridfinity.py` module — never hand-roll the base profile.

```python
from gridfinity import GridfinityBin
bin = GridfinityBin(grid_x=3, grid_y=2, height_units=3, stacking_lip=True)
bin.add_pocket(length=88.6, width=72.6, corner_r=(12.0, 1.0))
result = bin.build()
```

> 📖 Full API & spec constants: `references/gridfinity.md`

## Utility Scripts

Scripts in `scripts/` — copy next to model script before running.

| Script | Purpose |
|--------|---------|
| `run_cadquery_model.py` | Run + preview + JSON result |
| `preview.py` | STL → multi-view PNG |
| `gridfinity.py` | Gridfinity bin generator |
| `mesh_io.py` | STL loading + validation |
| `stl_to_3mf.py` | STL → 3MF converter |
| `outline_from_scan.py` | Scan → pocket outline |

> 📖 Full usage: `references/utility-scripts.md`

## Delivery Checklist

- [ ] Parameterized (no magic numbers)
- [ ] Printable (wall ≥ 1.2mm, overhangs < 45°, flat bottom)
- [ ] Preview inspected + watertight
- [ ] STL + preview PNG delivered
- [ ] Print recommendations (material, orientation, supports)
- [ ] Parameter table offered for tweaks
