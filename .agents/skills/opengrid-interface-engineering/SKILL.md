---
name: opengrid-interface-engineering
description: Design, adapt, inspect, and validate openGrid-compatible interfaces for removable 3D-printed components. Use when creating a new wall, desk, crate, shelf, electronics enclosure, or other object with openGrid, openConnect, Multiconnect, Lite/Full snaps, or cross-ecosystem mounting. Require authentic upstream mating geometry and measured fit results.
---

# openGrid interface engineering

## Objective

Extend the repository with **reusable, authentic, physically testable** mounting interfaces while keeping dimensioned designs modular and printer-agnostic.

Read `AGENTS.md`, `config/standard.json`, `docs/INTERFACES.md`, and `references/interface-contract.md` before designing a connector. Source geometry is the upstream official openGrid/openConnect model; never treat the starter's square openings or pitch-aligned holes as proven snap profiles.

## Workflow

1. **Choose the joint's job.** Differentiate removable accessory mounting, panel alignment, structural corner reinforcement, and actual fasteners. Don't use an accessory snap as a load-bearing structural joint.
2. **Select and acquire a native interface.** Use the matching upstream **Full or Lite** snap, openConnect head/slot, or Multiconnect interface. Download its original editable CAD, record URL, version/commit, license, print orientation, and whether it fits the intended board. Don't recreate geometry from screenshots, inferred dimensions, or AI approximation.
3. **Parameterize the new object.** Keep cell-center pitch **exactly 28 mm (1.1024 inches)** internally; expose human-facing sizes in inches and weights in pounds. Distinguish object size, snap spacing, panel thickness, and measured tolerances. Preserve the native connector geometry rather than scaling it indiscriminately.
4. **Integrate the mating part.** Merge upstream source geometry with `cad/library.py` parts. Check solid/watertight validity, adequate material around inserts, orientations, support requirements, printer envelope, and assembly interference.
5. **Software-test the interface.** Use BRep intersection / spatial checks, print and slicer previews, and an explicit small test coupon. These are CAD/preflight checks, not proof the snap fits.
6. **Physical fit-test.** Print against a genuine Full or Lite openGrid sample. Record insertion, repeatable removal, retention, wear, material, layer orientation, actual nominal/observed clearances, and print profile. Never claim a load capacity without a controlled test.
7. **Publish reusable components.** Assign versioned `interface_id`, add complete provenance and validation record, update `config/catalog.json`, and document the new public interface. Mark `fit_verified: true` only with actual test evidence.

## Output contract

Provide source CAD, STEP, STL, editable parameters, provenance, measured print/slicer results, validation state, and a small manual assembly/test checklist.

Explicit statuses: `cad_valid`, `slicer_verified`, `fit_verified`, `load_tested` are independent. Never infer later statuses from earlier ones. A component remains experimental until tested.

## Safety

No overhead/loft support, high-risk loads, or implied structural ratings. Ask for or verify real equipment dimensions before asserting an accessory fits. A new object can integrate the same standard only if the actual mating interface has been built and verified.

## Resources

- `references/interface-contract.md`: reference source selection and tolerance workflow
- `references/fit-test-template.json`: versionable physical evidence template
- `https://www.opengrid.world/guides/modeling/`
- `https://www.opengrid.world/guides/snaps/`
- `https://github.com/mitufy/opengrid-projects/tree/main/lib`
