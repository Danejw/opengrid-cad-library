# openGrid Physical Systems Starter Library, v0.1

A small, extensible, **code-driven parametric CAD starter** for making reusable physical objects built around the openGrid 28 mm (about **1.10 inch**) grid. Created for a compact maker bedroom and two wall installations.

**Status:** The wall layout planner and four independently printable CAD prototypes work now. They have been generated and software-checked for solid geometry. The **real openGrid mating snaps are intentionally not approximated**. To produce certified wall-mounted accessories, import the **publisher's exact bare snap or openConnect slot source** and run a physical fit test.

This distinction prevents future AI agents from inventing incompatible "openGrid-shaped" connectors.

## What's here

| File | Purpose | Output | Connection status |
|---|---|---|---|
| `cad/wall_planner.py` | Accurate 28 mm grid layout for both walls | SVG, CSV, JSON | Exact grid pitch, no connector geometry |
| `cad/library.py` `test_pitch_coupon()` | Check 28 mm print spacing and dimensional accuracy | STEP + STL | Measurement coupon only, **not** snap-compatible |
| `cad/library.py` `grid_tray()` | Desk tray, with rear mounting tab and standardized hole-center spacing | STEP + STL | Tray functions by itself; wall attachment must be engineered using native snap |
| `cad/library.py` `vented_crate()` | One-piece storage crate, openGrid-aligned window spacing | STEP + STL | Standalone crate; windows **do not** accept openGrid snaps |
| `cad/library.py` `adapter_blank()` | Mounting plate with a pitch-aligned hole pattern | STEP + STL | Blank intended for adding verified external snap geometry |
| `config/standard.json` | Machine-readable dimensional and interface policy | JSON | Exact verified public dimensions |
| `docs/INTERFACES.md` | Genuine upstream connector integration instructions | Markdown | Source links and validation gates |
| `AGENTS.md` | Rules for AI/CAD agents building new modules | Markdown | Reuse contracts and safety gates |

All examples fit within **7.1 × 7.1 inches** in plan, so they fit both the A1 and A1 Mini build plates by nominal dimensions. Confirm actual clearances in your slicer. The tray and crate are one-piece models. Editable STEP and printable STL files are generated from the source code, or downloaded as artifacts from a successful GitHub Actions build.

## Quick start

Run this in a terminal (Python 3.11+ recommended):

```bash
python -m pip install -r requirements.txt
python cad/generate.py --part all
python cad/wall_planner.py --printer a1
python cad/wall_planner.py --printer a1-mini
python -m pytest -q tests
```

Open the exported `.step` files in Fusion or other STEP-aware CAD. Use Bambu Studio to load the `.stl` files and check print estimates. Edit `cad/library.py` to change dimensions or make new reusable objects.

## Your room's two wall layouts

| Wall | Actual size | Complete-cell layout | Coverage | Remaining edge space | A1 panels (8×8 cell max) | A1 Mini panels (6×6 cell max) |
|---|---|---|---|---|---:|---:|
| A | 64 × 64 in | 58 × 58 cells | 63.937 × 63.937 in | 0.063 × 0.063 in | 64 | 100 |
| B | 54 × 60 in | 48 × 54 cells | 52.913 × 59.528 in | 1.087 × 0.472 in | 42 | 72 |

All coverage dimensions refer to grid spacing with the wall's lower-left origin. Center the completed grid to distribute the border equally if preferred. This is **tile planning**, not a final count of screws, printed connectors, plastic weight, or required structural fasteners. Generate wall panels from the **official** openGrid tile generator and verify exact exterior dimensions before printing all tiles.

The A1 can nominally fit 9 × 9 cells (9.92 × 9.92 inches), but that leaves almost no margin; the default is conservative **8 × 8 cells (8.82 × 8.82 inches)**. A1 Mini default: **6 × 6 cells (6.61 × 6.61 inches)**.


## Get print-ready exports from GitHub

Open [GitHub Actions](https://github.com/Danejw/opengrid-cad-library/actions/workflows/build-cad.yml) and select a successful **Build and validate parametric CAD** run. Download the `opengrid-cad-library-v0.1-exports` artifact. It includes four prototype STL/STEP pairs plus layouts for both walls and both printer sizes.

You can also run the Quick start commands locally to regenerate the exact outputs. Generated exports are not committed as binaries so changes to the source remain reproducible and the repository stays lightweight.

## Design principles

1. **One reusable grid:** Keep all mounting cell centers at 28 mm increments, even in crates, shelves, desk accessories, and walls.
2. **One real mating interface:** Use publisher-authored geometry for production openGrid snaps, openConnect slots, and Multiconnect. Never fake exact snap profiles.
3. **Independent structural joints:** Use properly designed joints for load-bearing crate corners, shelves, and furniture. openGrid accessory snaps are not automatically structural connectors.
4. **Parametric modules:** Store relevant dimensions as variables and generate editable CAD. Keep units clearly labeled.
5. **Version + provenance:** Document upstream interface source, printer, filament, tolerance, and results for each validated mating connector.

## Print validation checklist

- Download an official openGrid **Lite** and **Full** test panel and the matching upstream snaps, then fit them physically.
- Print `output/pitch_coupon.stl` to measure whether the printer reproduces 28 mm spacing. It is a measurement artifact, not a snap test.
- Print `output/grid_tray.stl` on the bed. It is usable standalone; do not hang it without designing and testing the actual wall connector.
- Measure real filament used in Bambu Studio. Do not infer accurate filament pounds from solid CAD volume because slicing, infill, and supports affect consumption.
- Test all loaded printed plastic parts before relying on them. Use screws into appropriate studs/anchors for wall installation.

## Links

- Official openGrid: https://www.opengrid.world/
- Official accessory modeling instructions: https://www.opengrid.world/guides/modeling/
- Official snap types: https://www.opengrid.world/guides/snaps/
- Official wall assembly: https://www.opengrid.world/guides/quickstart/
- Official panel files: https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem
- openConnect reference: https://github.com/mitufy/opengrid-projects/tree/main/lib

## Licensing

This package's **new** Python code and documentation are provided under MIT, see `LICENSE`. It does **not** redistribute or relicense the publisher's original openGrid models, snap files, or other upstream projects. Those remain under their respective licenses. Credit and follow any conditions if you download/remix their native geometries.
