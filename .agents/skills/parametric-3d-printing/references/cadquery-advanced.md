# CadQuery Advanced Reference

## BRep vs CSG Mindset

CadQuery uses **Boundary Representation (BRep)**: a model is defined by its surfaces, edges, and vertices — not by Boolean operations on primitives. The CSG reflex (union/cut everything) produces brittle, unidiomatic code.

**Wrong reflex (CSG):**
```python
result = base.union(cq.Workplane().box(10, 10, 5).translate((0, 0, 10)))
```

**Right reflex (BRep):**
```python
result = base.faces(">Z").workplane().rect(10, 10).extrude(5)
```

Only reach for `.union()`, `.cut()`, or `.intersect()` when you genuinely need to combine separate solids.

## Two APIs — Know Which One

**Fluent (Workplane) API** — chains operations with hidden state (current plane, stack). Best for parts built up from sketches and feature operations.
```python
import cadquery as cq
result = cq.Workplane("XY").box(10, 10, 10).faces(">Z").hole(3)
```

**Free Function API** — no hidden state, all operations explicit. Boolean ops as operators: `+` (union), `-` (cut), `*` (intersect).
```python
from cadquery.func import *
b = box(10, 10, 10)
result = b - cylinder(1.5, 10)
```

**Do not mix the two styles** unless you explicitly convert with `.val()`.

## Selectors Reference

| Selector | Meaning |
|----------|---------|
| `">Z"` | Highest centroid along Z |
| `"<Z"` | Lowest centroid along Z |
| `"\|X"` | Normal parallel to X axis (both directions) |
| `"#Z"` | Normal/direction orthogonal to Z |
| `"+Z"` | Normal points in +Z direction |
| `"-Z"` | Normal points in -Z direction |
| `">>Z[1]"` | Second item sorted ascending by Z (0-indexed, fragile!) |
| `"%Plane"` | Planar faces |
| `"%Cylinder"` | Cylindrical faces |
| `"%Circle"` | Circular edges |
| `"not >Z"` | Inverts selector |
| `">Z and \|X"` | Combines selectors (AND) |
| `">Z or <Z"` | Combines selectors (OR) |

**Tag-based selection (preferred for stability):**
```python
result = (
    cq.Workplane("XY")
    .box(10, 10, 10)
    .faces(">Z").tag("top")
    .end()
    .faces(tag="top").workplane().hole(3)
)
```

**Warning:** Index selectors (`">>Z[1]"`) shift after adding fillets/features. Always prefer tags or geometric selectors.

### How Selectors Match

- `">Z"` returns the face with the highest **centroid** Z — not the face containing the highest vertex.
- `"|Z"` selects faces with normal **parallel** to Z (top AND bottom on a box). Use `">Z"` for top only.
- `"#Z"` selects entities **orthogonal** to Z (side faces, horizontal edges).
- Chaining (`.faces(">Z").edges("%Circle")`) is clearer than combining in a single string.

## Workplane Rules

- `.workplane()` resets the 2D origin to the selected face center (controlled by `centerOption`)
- After `.workplane()`, coordinates are **local** to that plane, not global
- Use `centerOption="CenterOfBoundBox"` when geometric center matters
- `centerOption="ProjectedOrigin"` (default) projects the parent origin — often NOT the face center
- `.transformed()` is cumulative within the current workplane context
- Always call `.workplane()` after face selection before sketching
- Use `.center(x, y)` to shift the 2D origin within the plane

**Cut direction gotcha:** The workplane normal points **outward** from the selected face. Use `invert=True` to cut into the solid:
```python
# Wrong: cuts upward away from the solid
solid.faces(">Z").workplane().circle(3).cutBlind(5)
# Correct: invert flips the normal into the solid
solid.faces(">Z").workplane(invert=True).circle(3).cutBlind(5)
```

**Common mistakes:**
- Forgetting `.end()` after `.tag()` — chain `.end()` to return to the solid context
- Operating on a face without `.workplane()` — `.circle().extrude()` needs a workplane; `.hole()` and `.shell()` don't
- Calling `.workplane()` without a prior face selection — ambiguous origin

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| `.cut(cylinder)` for a hole | `.faces(...).hole(d)` |
| `.cut(shell_solid)` to hollow | `.faces(...).shell(thickness)` |
| `.union(chamfered_edge)` | `.edges(...).chamfer(d)` |
| Index selectors `">>Z[1]"` | Tag faces early, use `tag="name"` |
| Hardcoded global coordinates | Use workplanes + `.center()` |
| Boolean in a loop | Combine into `compound()` first, then subtract once |
| Missing `.close()` before extrude | Always close wire profiles |
| Forgetting `.end()` after `.tag()` | Chain `.end()` to return to solid context |
| `BREP_API command not done` | Fillet radius too large, self-intersecting profile, or shell too thick |
| `.translate()` in fluent chain | Use `.center()` or `cq.Plane(origin=...)` instead |
| `combine=True` (default) then `.union()` again | Produces double union — set `combine=False` if separate |

### BREP_API command not done — Detailed Fixes

This OpenCASCADE kernel error means the requested geometry is invalid:
- **Fillet/chamfer radius too large**: Reduce radius; must be < shortest adjacent edge. Apply different edge groups separately.
- **Adjacent fillets overlap**: Fillet in separate calls, smallest first.
- **Self-intersecting profile**: Wire crosses itself, or revolve profile crosses the axis.
- **Sweep profile too large**: Profile folds back on itself at tight path curvature.
- **Shell thickness too large**: Offset surface self-intersects; reduce thickness.

## Free Function API Reference

```python
from cadquery.func import *

# Primitives
box(w, h, d), cylinder(r, h), sphere(r), cone(r1, r2)
plane(w, h), circle(r), rect(w, h), segment(p1, p2)

# Construction
wire(e1, e2, ...), face(wire), solid(f1, f2, ...), shell(f1, f2, ...)
compound(s1, s2, ...)

# Operations
extrude(profile, direction_vector)
loft(e1, e2, e3, cap=False)
sweep(profile, path)
revolve(face, axis_point, axis_dir, angle)

# Placement (no workplane needed)
shape.moved(x=1, y=2, z=3)     # translate
shape.moved(rx=90)              # rotate (degrees)
shape.moved((1,0,0), (5,0,0))  # multiple copies → compound
shape.move(z=5)                 # in-place variant

# Boolean operators
a + b   # fuse/union
a - b   # cut/difference
a * b   # intersect
a / plane  # split
```

### Adding Features Without Booleans (performance)

```python
from cadquery.func import *

b = box(w, w, w)
b_bot = b.faces('<Z')
b_top = b.faces('>Z')
inner = extrude(circle(r), (0, 0, w))

b_bot_hole = b_bot.addHole(inner.edges('<Z'))
b_top_hole = b_top.addHole(inner.edges('>Z'))

result = solid(
    b.remove(b_top, b_bot).faces(),
    b_bot_hole, inner, b_top_hole,
)
```

## Common Fluent API Patterns

**Polar pattern:**
```python
result = (
    cq.Workplane("XY")
    .cylinder(5, 20)
    .faces(">Z").workplane()
    .polarArray(radius=8, startAngle=0, angle=360, count=6)
    .hole(2, depth=8)
)
```

**Rectangular pattern:**
```python
result = (
    cq.Workplane("XY")
    .box(40, 40, 10)
    .faces(">Z").workplane()
    .rarray(xSpacing=10, ySpacing=10, xCount=3, yCount=3, center=True)
    .hole(3, depth=8)
)
```

**Revolve:**
```python
result = (
    cq.Workplane("XZ")
    .moveTo(5, 0).lineTo(5, 10).lineTo(8, 10).lineTo(8, 0).close()
    .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
)
```

**Loft between profiles:**
```python
result = (
    cq.Workplane("XY")
    .rect(20, 10)
    .workplane(offset=15)
    .circle(6)
    .loft()
)
```

**Sweep along a spline path:**
```python
path = cq.Workplane("XZ").moveTo(0, 0).spline([(10, 5), (20, 0)], includeCurrent=True)
result = cq.Workplane("YZ").circle(2).sweep(path)
```

**Reusable sketch with `.placeSketch()`:**
```python
slot = cq.Sketch().slot(8, 3)
result = (
    cq.Workplane("XY")
    .box(40, 20, 8)
    .faces(">Z").workplane()
    .placeSketch(
        slot.moved(cq.Location((-10, 0, 0))),
        slot.moved(cq.Location((10, 0, 0))),
    )
    .cutBlind(-4)
)
```

**Shell a solid (open-top box):**
```python
result = cq.Workplane("XY").box(30, 20, 15).faces(">Z").shell(-2)
```
Note: `.shell()` can be buggy with complex profiles. For reliable hollowing, prefer boolean subtraction (see print-rules.md).
