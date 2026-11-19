# Progressive Preview Workflow

Build the model in phases. At each phase, export an STL, render a preview, self-review it, then **show it to the user and ask for feedback** before proceeding. This catches problems early and keeps the user involved.

## Preview Recipe (use at every phase)

**One-shot (run script + render + parse result as JSON):**
```bash
python3 run_cadquery_model.py model.py --preview --strict
```
This executes `model.py`, finds the STL it wrote, renders the multi-view preview, and emits a JSON result with `success`, `stdout`, `stderr`, `stl`, `preview`, and `watertight`. With `--strict`, a non-watertight mesh is a hard failure. Use this as the default loop: if `success` is false, read the `stderr` field to fix the CadQuery script, then re-run.

**Rendering only (when the STL already exists):**
```bash
python3 preview.py model.stl preview.png --views multi
```

Then view the preview image, self-review it against the design review checklist, and fix any issues you spot **before** showing it to the user.

---

## Phase 1: Base Shape

Build the basic outer form: overall dimensions, shell/walls, bottom plate. No cutouts, no fillets, no details yet.

1. Write the script with parameters and basic geometry
2. Export STL and render preview
3. Self-review: Does the shape and size look right? Is the bottom flat for printing?
4. **Show the preview to the user**: "Here's the basic shape. Does this look right before I add details?" Include key dimensions.
5. Wait for feedback. If the user wants changes, iterate here before moving on.

## Phase 2: Features

Add functional details: holes, cutouts, mounting bosses, cable slots, ventilation, snap-fits, internal structures.

1. Add features to the script
2. Export STL and render preview
3. Self-review: Are all features visible? Do booleans look clean? Are holes in the right positions?
4. **Show the preview to the user**: "I've added [list features]. Anything to change before I finalize?"
5. Wait for feedback. Iterate if needed.

## Phase 3: Final Delivery

Apply finishing touches: fillets, chamfers, edge cleanup. Do a full printability review.

1. Add fillets/chamfers (largest radius first, apply after shell)
2. Export final STL and render preview
3. **Full self-review** using the complete design review checklist: visual inspection, dimensional verification, printability analysis
4. Fix any issues found, re-export if needed
5. **Deliver to the user**: final STL + preview image + print recommendations (orientation, supports, infill, material notes)

---

**Important:** Do NOT skip phases or combine them unless the model is very simple (e.g., a flat bracket with two holes). For anything with enclosed geometry, multiple features, or tight tolerances, follow all three phases.

## Print Recommendations (final delivery)

When you deliver the final STL, always include a one-line slicer recipe plus a short rationale. Bambu Studio, PrusaSlicer, and OrcaSlicer already set sensible defaults from their filament + process presets, so **do not restate every slicer option**. Only tell the user what matters for *this* model: material, layer height, walls, infill, supports, and orientation.

**Baseline recipe (0.4mm nozzle, typical FDM):**
> PLA, 0.2mm layer, 2 walls, 15% gyroid infill, no supports, orientation: flat side on bed.

**When to deviate from the baseline:**
- **Load-bearing brackets / hooks / hinges**: bump infill to 25-40%, 3-4 walls, consider PETG over PLA for toughness.
- **Thin decorative walls or vases**: 0 infill, vase mode or 1 wall.
- **Tall narrow parts**: add a brim for bed adhesion.
- **Flexible parts (gaskets, grips)**: TPU 95A, 0.2mm layer, slower speed, no supports.
- **Functional overhangs the geometry can't avoid**: tree supports, or call them out so the user knows.
- **Outdoor / hot environments**: PETG or ASA, not PLA.
- **Food / skin contact**: call out that FDM parts are not food-safe and recommend a food-safe coating.

**Format at delivery time:**
```
Print settings: PLA, 0.2mm layer, 2 walls, 15% gyroid infill, no supports.
Orientation: place flat back side on the bed (front face up).
Why: the case has no overhangs above 45°, and 15% infill is plenty for a
TPU-adjacent protective shell.
```

Keep it to ~3 lines. Never dump every slicer setting; the slicer already knows.
