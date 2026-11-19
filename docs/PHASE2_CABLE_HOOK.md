# Phase 2: native openConnect cable hook (prototype)

This is the first **functional accessory** for the library. It uses a native upstream **2 × 1-cell openConnect receiving plate** from Phase 1 as the actual mating surface. A lightweight cable-hanging peg is fused to its opposite side in editable OpenSCAD source.

Approximate dimensions: a 2.76-inch × 1.65-inch native receiver carrying 2 × 1 openConnect slot positions, plus a 0.75-inch peg with a 0.50-inch retaining lip. Exact STL geometry is machine-generated and verified in CI.

## Generate

```bash
python cad/opengrid/generate_interfaces.py --variant all
python cad/opengrid/generate_accessory.py --stem-length-in 0.75 --stem-diameter-in 0.30 --lip-diameter-in 0.50
python cad/opengrid/validate_accessory.py
```

Or download the CI artifact. The editable source is `cad/opengrid/cable_hook.scad`; the completed STL is `output/accessories/opengrid_openconnect_cable_hook.stl`. A STEP export of the **complete native assembly** is not yet provided because OpenSCAD's STL-based assembly does not preserve analytic BRep faces; don't mistake a mesh conversion for native parametric STEP.

## How to mount

Use a matching native openConnect snap/head produced by Phase 1, secured in an actual openGrid Full or Lite panel, then mate the accessory plate to it through the native openConnect receiver geometry. Follow the manufacturer's assembly direction. Test the insertion sequence and retention on real prints before using loaded.

## Qualification status

- Source geometry: unchanged upstream native receiving plate.
- Design: 3D printed cable peg attached to plate.
- Software: geometry and manifold checks in CI.
- Slicer prep: pending actual printer/material/toolpath profile.
- Physical fit: **unverified**.
- Strength: **unverified**. Suitable only as a lightweight prototype until tested.

If the prototype doesn't print or mate successfully, keep the failure record and correct the design before treating this as reusable production geometry.
