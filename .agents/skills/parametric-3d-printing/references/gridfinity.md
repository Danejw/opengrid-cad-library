# Gridfinity Module Reference

For any Gridfinity request (bins, inserts, cradles for the 42mm modular grid system), **use the bundled `gridfinity.py` module; never hand-roll the base profile**. The module is tested, spec-compatible (base profile, stacking lip, 6x2mm magnet bores, M3 screw holes on the 26mm square), and validates parameters with actionable errors.

## Workflow

1. Copy `gridfinity.py` from this skill's `scripts/` directory next to the model script (vendored module; scripts must stay runnable standalone).
2. Build with the `GridfinityBin` API (see below).

## Usage Example

```python
import cadquery as cq
from gridfinity import GridfinityBin

bin = GridfinityBin(grid_x=3, grid_y=2, height_units=3,
                    stacking_lip=True, magnets=False)
bin.add_pocket(length=88.6, width=72.6, corner_r=(12.0, 1.0))  # cradle
# or: bin.add_compartments(cols=3, rows=2, scoop_r=6, label_tab=True)
# or: bin.add_polygon_pocket(points, depth=15, clearance=0.3)
# or: bin.add_cylinder_pocket(diameter=22, center=(42, 27),
#         tilt=35, tilt_dir=(-1, 0), round_bottom=True)
# or: bin.add_finger_notch(side="+Y", width=20, offset=40)
result = bin.build()
cq.exporters.export(result, "my_bin.stl", tolerance=0.01, angularTolerance=0.1)
print(bin.summary())
```

## API Reference

### Constructor

```python
GridfinityBin(grid_x, grid_y, height_units,
              stacking_lip=True, magnets=False, screws=False, floor_t=2.0)
```

### Methods

| Method | Description |
|--------|-------------|
| `.add_pocket(length, width, depth=None, corner_r=2.0, center=(0,0))` | Rounded-rect cavity. `corner_r`: scalar, 2-tuple (-X end, +X end), or 4-tuple |
| `.add_polygon_pocket(points, depth=None, clearance=0.0)` | Arbitrary outline cavity. Points are (x,y) mm list |
| `.add_cylinder_pocket(diameter, depth=None, center=(0,0), tilt=0, tilt_dir=None, round_bottom=False)` | Round cavity. Tilt for thumb scoops (max 45°) |
| `.add_compartments(cols=1, rows=1, wall_t=1.2, scoop_r=0, label_tab=False, label_d=12)` | Classic divided storage |
| `.add_finger_notch(side="+X", width=20, depth=None, offset=0)` | U-shaped scallop in side wall |
| `.build()` | Validate and return `cq.Workplane` (bottom at Z=0) |
| `.summary()` | Description string with all dimensions |

### Properties

| Property | Description |
|----------|-------------|
| `.outer_w` | Outer width (grid_x × 42 - 0.5mm) |
| `.outer_d` | Outer depth (grid_y × 42 - 0.5mm) |
| `.nominal_h` | height_units × 7mm |
| `.total_h` | nominal + lip (4.75mm if stacking_lip) |
| `.floor_z` | Z of interior floor (base profile + floor_t) |
| `.max_depth` | Deepest possible cavity from rim |

### Spec Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| `GRID_PITCH` | 42mm | Cell pitch |
| `HEIGHT_UNIT` | 7mm | One height unit |
| `CLEARANCE` | 0.25mm | Per side → 41.5mm footprint |
| `BASE_H` | 4.75mm | Base profile height |
| `CORNER_R` | 3.75mm | Body corner radius |
| `MAGNET_D` | 6.5mm | Bore for 6×2mm magnets |
| `SCREW_D` | 3.0mm | M3 thread-forming |
| `HOLE_SPACING` | 26mm | Magnet/screw centers per cell |

## Design Tips

- **Sizing a pocket:** add 0.3mm per side fit clearance, +1mm per side for easy drop-in/out.
- **Pocket from scan:** use `outline_from_scan.py` to extract max cross-section from an STL scan.
- **Height choice:** whatever holds contents; contents may protrude above the rim.
- **Magnets:** `magnets=True` needs a magnetic baseplate; skip for drawer bins.
- **Error handling:** `GridfinityError` is raised with specific messages. Fix parameters, don't bypass validation.
- **Unsupported features:** For baseplates or odd lips, fall back to custom geometry but use the spec constants from `gridfinity.py` as source of truth.
