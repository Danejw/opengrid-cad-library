# Native interface contract

**Core:** openGrid cell pitch 28 mm, 1.10236 inches. Native Full thickness 6.8 mm (0.268 in); Lite 4 mm (0.157 in). Use publisher's geometry and check specific connector/board compatibility.

## Interface definition fields

- `interface_id`, `upstream_url`, `upstream_revision`, `license`, `geometry_file`
- `board_variant`: Full, Lite, both (verified), or unknown
- `connector_type`: normal / directional / locking snap / openConnect / Multiconnect / mounting screw
- `cell_spacing`: exact 28 mm basis (do not translate 1.1 in back to metric for internal CAD)
- `purpose`: accessory mount, fastening, structural, alignment; do not conflate purposes
- `printer`, `nozzle`, `filament`, `orientation`, `slicer_profile`, `tolerances`, `test_evidence`
- Independent status gates for software model, slicer, physical fit, and load.

## Build-integration approach

For STEP, import the upstream connector body to the BRep kernel and join it to a new part if geometry and licensing permit. For editable OpenSCAD source, use upstream library functions or export and transfer native geometry. Keep the original source revision pinned.

A board's repeating opening is not necessarily a structural connector. Designing a crate with openGrid-like windows does not magically make it compatible with an existing wall snap.

## Acceptance tests

1. Reference import: valid geometry and fixed source hash or file version.
2. Pitch fit: check exact center spacing, alignment, and part bounding box.
3. Collision checks: verify full insertion path and locking/free-clearance zones.
4. Slicer: inspect unsupported features and stiffness-sensitive layer orientation.
5. Physical: five insert/remove cycles minimum for the first proof, visually inspect stress whitening and deformation.
6. Retention and load: state whether measured with a controlled test; no untested strength claims.
7. Record all pass/fail observations; if a tolerance workaround succeeds, document it for next agent.

When in doubt, print a minimal interface calibration sample first. A simple successful test is more valuable than sophisticated unverified simulation.
