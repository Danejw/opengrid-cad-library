# Agent contract: openGrid physical CAD library

Goal: create modular, composable, reusable physical accessories and assemblies compatible with openGrid's real interfaces, and preserve proven designs for future builds.

## Source of truth

- Public publisher-authored geometry: official openGrid and upstream openConnect models listed in `docs/INTERFACES.md`.
- Internal geometry: `cad/library.py` and `config/standard.json`.
- Physical validation evidence: create per-part build records after real printing; software-rendered solids alone are insufficient.
- Human-facing dimensions in **inches/feet** and material weights in **pounds**. Internal CAD values in millimeters only where required to match the official reference geometry.

## Rules

1. Prefer a generic configurable module over cloning an isolated fixed-size item.
2. Every design should expose a clear set of dimensions, interface locations, and versioned part IDs.
3. Treat the 28 mm (1.1024 inch) openGrid spacing as an exact reference. Document off-grid exceptions.
4. **Do not approximate load-bearing connectors or openGrid mating snap profiles**. Import official snap or negative-slot CAD and retain upstream provenance. Do not claim a snap-in print is compatible until it is physically tested.
5. Any object larger than the printer bed must have a documented split and joining strategy. Accessory connectors and structural fasteners have distinct jobs.
6. New parts should be exportable as STEP and STL; test for solid validity, closed watertight meshes, and slicer fit.
7. Distinguish: CAD-valid, slicer-verified, assembled, fit-verified, load-tested. Do not infer load limits without tests.
8. No design shall structurally support the bed/loft or present unsupported safety load ratings.
9. Record actual filament consumption from the slicer, in pounds, not guessed from CAD volume.
10. Before changing a base interface, test against previously validated parts and document breakage risks.

## Naming

Name objects `{system}-{function}-{version}`, e.g. `og-tray-v1`; name separate adapters by both source and destination interfaces.

## Initial build order

1. Official 2x2 Lite/Full panels plus original snaps; verify real insertion and removal.
2. Pitch calibration plate, `pitch_coupon.stl`, to measure dimensional accuracy.
3. Desk tray and crate; verify straightforward independent printing.
4. Add native snap/slot to a copy of `adapter_blank.step`, validate fit, and save that as the first approved reusable mating interface.
5. Reuse the approved interface on shelf, closet organizers, underdesk accessories, and future AI-generated objects.

## Skills and MCP tool selection

Before starting a specialized engineering task, see `docs/SKILL_ROUTER.md` and read the smallest relevant `.agents/skills/<name>/SKILL.md`. The repository contains upstream mechanical skills, the official OrcaSlicer MCP skill instructions, an upstream skill-creator, and project-specific skills for openGrid, Fusion MCP, Bambu Studio, FreeCAD/OpenSCAD, and mesh validation.

**Skills teach methods; MCP provides actions; installed applications execute them.** Confirm a tool is available and authorized before claiming to have used it. The recommended system architecture and official integrations are documented in `docs/MCP_INTEGRATIONS.md`.

For openGrid connector work, **always** load `opengrid-interface-engineering`, use exact upstream geometry, and collect real-world fit evidence. For any 3D-print job, use `mesh-validation` and the applicable slicer skill. Never start a print or use a paid cloud backend without explicit authorization for that action.

Vendored skills retain their upstream licenses; see `docs/THIRD_PARTY_SKILLS.md`. Independently review third-party executable scripts before running them. Don't automatically load or execute every skill.
