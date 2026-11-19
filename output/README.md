# Generated CAD exports

This directory is intentionally source-controlled without binary-generated STEP/STL files or wall-specific layout files. Regenerate all exports locally with:

```bash
python -m pip install -r requirements.txt
python cad/generate.py --part all
```

To generate a wall plan, supply your measured width and height in inches:

```bash
python cad/wall_planner.py --printer a1 --width "$WIDTH_IN" --height "$HEIGHT_IN"
```

Wall-specific layouts are not generated in GitHub Actions and aren't committed to the repository.

Or open GitHub Actions -> **Build and validate parametric CAD** -> the latest successful run -> download the **opengrid-cad-library-v0.1-exports** artifact.

Generated examples are CAD-valid prototypes, but their openGrid snap interfaces have **not** been validated on physical hardware. See `docs/INTERFACES.md`.
