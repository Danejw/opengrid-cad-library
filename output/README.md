# Generated CAD exports

This directory is intentionally source-controlled without binary-generated STEP/STL files or large wall-layout SVG files. Regenerate all exports locally with:

```bash
python -m pip install -r requirements.txt
python cad/generate.py --part all
python cad/wall_planner.py --printer a1
python cad/wall_planner.py --printer a1-mini
```

Or open GitHub Actions -> **Build and validate parametric CAD** -> the latest successful run -> download the **opengrid-cad-library-v0.1-exports** artifact.

Generated examples are CAD-valid prototypes, but their openGrid snap interfaces have **not** been validated on physical hardware. See `docs/INTERFACES.md`.
