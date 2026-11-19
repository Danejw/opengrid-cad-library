# Design Review Checklist

## Visual Inspection

- [ ] Overall shape matches request
- [ ] All features present (holes, cutouts, mounts, etc.)
- [ ] Proportions look correct
- [ ] No floating or disconnected geometry
- [ ] Flat bottom for printing
- [ ] No extreme overhangs visible
- [ ] Fillets/chamfers applied correctly
- [ ] Wall thickness appears sufficient
- [ ] Interior properly hollowed (if applicable)
- [ ] Dimensions match requirements (check footer)

## Dimensional Verification

```python
import cadquery as cq

# After building the model:
bb = result.val().BoundingBox()
print(f"Width  (X): {bb.xlen:.1f} mm")
print(f"Depth  (Y): {bb.ylen:.1f} mm") 
print(f"Height (Z): {bb.zlen:.1f} mm")
print(f"Volume: {result.val().Volume():.0f} mm³")

# Check specific dimensions
assert abs(bb.xlen - expected_width) < 0.1, f"Width mismatch: {bb.xlen} vs {expected_width}"
```

## Watertight Check

Non-watertight meshes are the most common cause of slicing failures:

```python
import trimesh

tm = trimesh.load("model.stl", force="mesh")
if tm.is_watertight:
    print("Mesh is watertight (good)")
else:
    print("WARNING: Mesh is NOT watertight — will cause slicing issues")
    # Common causes: unclosed shells, boolean artifacts, zero-thickness faces
```

## Printability Analysis — Overhang Detection

```python
import trimesh
import numpy as np

def check_overhangs(stl_path, max_angle=45):
    """Check for faces with overhang angle beyond threshold."""
    tm = trimesh.load(stl_path, force="mesh")
    normals = tm.face_normals
    downward = normals[:, 2] < 0
    if not downward.any():
        return 0.0
    down = np.array([0, 0, -1])
    down_normals = normals[downward]
    cos_angles = np.dot(down_normals, down) / (
        np.linalg.norm(down_normals, axis=1) + 1e-10)
    angles_from_down = np.degrees(np.arccos(np.clip(cos_angles, -1, 1)))
    overhang_from_horizontal = 90 - angles_from_down
    problem_faces = np.sum(overhang_from_horizontal > max_angle)
    return problem_faces / len(normals) * 100

pct = check_overhangs("model.stl")
if pct > 5:
    print(f"WARNING: {pct:.0f}% faces may need supports")
else:
    print(f"OK: Model looks printable without supports ({pct:.1f}% overhang)")
```

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Feature not visible in preview | Boolean operation failed silently | Check that cutting bodies overlap the main body |
| Walls are paper-thin | Shell thickness too small | Verify shell direction and thickness >= 1.2mm |
| Standoffs appear disconnected | Union failed (no overlap) | Ensure standoff base intersects with floor/wall |
| Cutout in wrong position | Coordinate system confusion | Use `centered=(True, True, False)` and verify offsets |
| Fillets look wrong | Radius too large for the edge | Reduce radius; must be < half smallest adjacent face |
| Dimensions are wrong in preview | Forgot to update a parameter | Add assertions comparing bounding box to expected dims |

## Output Checklist (before delivery)

- [ ] All dimensions are parameterized (no magic numbers)
- [ ] Wall thickness >= 1.2mm
- [ ] Designed for printability (minimal overhangs/supports)
- [ ] Print orientation noted in comments
- [ ] STL exported and file size is reasonable (not 0 bytes)
- [ ] Clear parameter names with units
- [ ] Script runs without errors
- [ ] Multi-view preview generated and visually inspected
- [ ] Preview shows correct shape, features, and proportions
- [ ] Bounding box dimensions match requirements
- [ ] Both STL and preview PNG delivered to user
