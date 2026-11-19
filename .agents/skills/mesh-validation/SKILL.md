---
name: mesh-validation
description: Run software preflight on 3D CAD/STL/3MF models including geometry integrity, orientation, bounding box, manifold/watertight status, print bed fit, and slicer verification.
---

# 3D-print mesh verification

Use this before calling an output `print-prepared`. Require an actual file to inspect. If available, inspect exact shape with CadQuery/OpenCascade and mesh with `trimesh` or the already-imported `parametric-3d-printing/scripts/mesh_io.py`.

Required checks: plausible inches-scaled bounding box; valid BRep; non-zero volume; a watertight manifold STL; no self-intersections / degenerate faces where checked; target printer build limits; chosen orientation and supports; repeatable export provenance. For assembly parts verify clearances and distinct object identities. Slicer mass in pounds comes only from actual slicing settings, not model volume estimates.

Report which software actually executed and what was inferred. The checks cannot establish mechanical strength or successful fit on a real openGrid snap. Reserve `fit_verified` for a physical test and `load_tested` for measured load evidence.
