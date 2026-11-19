# Phase 3: reproducible generation, geometry validation and preview pipeline

Runs in GitHub Actions using pinned native source and BOSL2, OpenSCAD, CadQuery, Trimesh and a virtual display for preview PNGs.

```text
Parametric source (Python/OpenSCAD)
  -> CadQuery 4 sample STEP + STL exports
  -> native Full, Lite and 2x1 receiver STL exports
  -> Phase 2 native-plate cable hook STL
  -> watertight/bounds/volume preflight
  -> eight 720x540 PNG CAD previews
  -> output/reports/engineering_report.json
  -> downloadable GitHub Actions artifact
```

**All generated physical interfaces are still prototype-level.** A successful CAD build validates the software model and its mesh. It is **not** a slicing result, print-completion record, insertion test, wear test, or validated strength rating.

The pipeline deliberately leaves filament use, print time, slicer-verification and fit-verification as `null` or `false` until those results are grounded by real software/tools and physical prints.

## Run manually

Prerequisites: Python dependencies in `requirements.txt`, OpenSCAD, BOSL2 (as pinned in CI), and `xvfb-run` on headless Linux.

```bash
python -m pytest -q tests
python cad/generate.py --part all
python cad/opengrid/generate_interfaces.py
python cad/opengrid/validate_interfaces.py
python cad/opengrid/generate_accessory.py
python cad/opengrid/validate_accessory.py
python cad/opengrid/release_pipeline.py
```

On Windows with an interactive OpenSCAD GUI you may replace `--xvfb xvfb-run` with a suitable local display wrapper or run `--no-preview` to generate the engineering report only.

## Next blocked phase: physical acceptance

Actual printing must wait for hardware and user approval. Use the native board + matching openConnect snap, verify insertion and removal, then record materials, slicer settings, measured print characteristics, failure modes, retention and repeatability. Only those tests can move `fit_verified` and `load_tested` to true.

Bambu Studio is a separately installed slicer, and Fusion MCP remains optional. GitHub Actions does not automatically connect to or control any printer.
