# Phase 1: genuine openGrid + openConnect interface

**Goal:** Keep a reusable source-pinned native connector and a compatible receiving plate, independently renderable for both Full and Lite board thicknesses.

- Original source: [mitufy/opengrid-projects](https://github.com/mitufy/opengrid-projects). openGrid created by David D, openConnect library and parametric generator by mitufy, published under Creative Commons Attribution 4.0. The six unchanged source files live in `vendor/mitufy-opengrid/`; see their Git blob hashes in `tests/test_native_interfaces.py`.
- Dependency: BOSL2, pinned to git revision `1351a9f7e5f30a95228e580d167fd4f2e184ad2c` in GitHub Actions.
- Renderer: OpenSCAD; variants `Full` (6.8 mm native source thickness) and `Lite` (4 mm), plus a **2 × 1 cell native receiving slot layout on a 70 × 42 mm (approximately 2.76 × 1.65 in) plate**. The fixture is for *openConnect*, which combines a native snap and accessory attachment head.
- Generated files: `output/interfaces/` contains STL variants, generated command manifest, and mesh verification JSON if the build succeeds.

**Setup:** Install OpenSCAD and BOSL2 so `include <BOSL2/std.scad>` resolves, or use the CI job. From the repo root:

```bash
python cad/opengrid/generate_interfaces.py --variant all
python cad/opengrid/validate_interfaces.py
```

## Source and testing claims

`source_pinned`: byte-for-byte source provenance verified by upstream Git SHA. This means **native geometry** is reused, not approximated.

`cad_valid`: only when OpenSCAD successfully exported 3 watertight solid STLs.

`slicer_verified`: only when a real slicer checks the target machine and profile.

`fit_verified`: only after the **physical** mating and removal cycle on a printed openGrid Full/Lite panel.

`load_tested`: only after a measured, controlled loading test.

All generated parts are **prototype-ready** but remain **unverified physically**. Wall mount screws, print orientation, dimensional shrinkage, filament and board variant affect real performance. The connector is intended as a removable *accessory* interface; it is not a structural shelf or furniture joint.

## Next step

Use this shared native interface to create a functional cable-management accessory in a separate Phase 2 commit.

CI uses the [official OpenSCAD 2026.07.20 AppImage](https://files.openscad.org/snapshots/) with its publisher-provided SHA256 check. The apt-packaged OpenSCAD 2021.01 produced a non-watertight Full variant and is not accepted as a verified rendering environment.
