# Print Rules & Common Pitfalls

## FDM Design Defaults

| Property | Minimum | Recommended |
|----------|---------|-------------|
| Wall thickness | 1.2mm | 2.0mm |
| Layer height | 0.08mm | 0.2mm |
| Hole clearance | 0.2mm | 0.3mm |
| Press-fit interference | 0.1mm | 0.15mm |
| Min feature size | 0.4mm (nozzle) | 0.8mm |
| Fillet radius (bottom) | 0.5mm | 1.0mm |
| Bridge span | - | < 20mm unsupported |
| Overhang angle | - | < 45° from vertical |

**Material-specific adjustments:**
- TPU: larger clearances (~0.5mm) due to flex
- PETG: stickier, add +0.1mm to fit clearances
- ABS: shrinks ~0.5-0.7%, scale critical dimensions up
- When in doubt, print a small test piece first

## Orientation Awareness

- Design with print orientation in mind
- Flat bottom surfaces print best
- Avoid supports when possible by designing around overhangs
- Add chamfers to bottom edges instead of fillets (fillets need supports)
- Comment the intended print orientation in the script

## CadQuery Print Patterns

**Hollow enclosure (boolean subtraction, preferred over `.shell()`):**
```python
outer = (
    cq.Workplane("XY")
    .box(width, depth, height, centered=(True, True, False))
    .edges("|Z").fillet(corner_r)
)
inner = (
    cq.Workplane("XY")
    .workplane(offset=floor_t)
    .box(width - 2*wall, depth - 2*wall, height, centered=(True, True, False))
    .edges("|Z").fillet(max(0.1, corner_r - wall))
)
result = outer.cut(inner)
```

**Screw boss:**
```python
.pushPoints([(x, y)])
.circle(boss_od / 2).extrude(boss_h)
.pushPoints([(x, y)])
.hole(screw_d + fit_clearance)
```

**Snap-fit clip:**
```python
# Cantilever beam with overhang hook
.workplane(offset=wall)
.moveTo(x, y).rect(clip_w, clip_l).extrude(clip_h)
# Add hook at tip with a small overhang (< 45 deg)
```

**Ventilation grid:**
```python
.pushPoints(vent_positions)
.slot2D(slot_l, slot_w).cutThruAll()
```

Other patterns: mounting brackets, cable routing channels, text/labels (`.text()`), multi-part assemblies with alignment pins.

## Common Pitfalls

### Hollowing: prefer boolean subtraction over `.shell()`
`.shell()` is fragile — fails on tapered bodies, lofted shapes, unions of multiple primitives, and anything with many fillets. The reliable pattern is boolean subtraction (see above). Only reach for `.shell()` when the body is a single simple primitive with uniform wall thickness.

### Build order: fillet → cut, not cut → fillet
Apply fillets while the geometry is still a clean primitive. Once you have cut holes/slots/pockets, filleting the resulting edges often fails or produces bad geometry. Same rule for chamfers.

### Fillet failures
Apply fillets from largest to smallest radius. **Do not wrap fillets in `try/except` to silently shrink the radius.** A fillet failure means the geometry or the radius is wrong — find the root cause.

### Zero-thickness geometry
Ensure boolean operations don't create infinitely thin walls. Add a small epsilon (0.01mm) when cutting bodies that are meant to pass just through a surface.

### Coordinate system
CadQuery centers geometry at origin by default. Use `centered=(True, True, False)` on `.box()` to place the bottom at Z=0 so `.faces("<Z")` is always the print bed.

### Hole direction
`.hole()` cuts through the entire part by default. Use `.cboreHole()` or `.cskHole()` for counterbore/countersink.

### Taper direction
In `.extrude(taper=angle)`, a **positive** taper angle narrows the shape (draft inward), **negative** flares it outward. This is opposite to what many expect.

### Loft is fragile
`.loft()` fails on many cross-section combinations. Prefer `.extrude(taper=angle)` when transitioning between a shape and a scaled version of itself. Only use `.loft()` for genuinely different profiles (e.g., circle to rectangle).

### Export errors / non-watertight STL
If export fails or the preview reports a non-watertight mesh, the geometry is invalid (usually self-intersecting booleans or zero-thickness faces). Fix the cause, don't paper over it. Run `python3 preview.py model.stl --strict` to fail loudly.
