# Reusable prompt to give a CAD agent

```text
You are working with the openGrid Physical Systems Starter Library. Read README.md, AGENTS.md, config/standard.json, and docs/INTERFACES.md before making changes.

Goal: design a parametric, reusable [OBJECT] for [USE CASE]. User-facing dimensions are in inches, filament mass in pounds, but keep the exact upstream 28 mm openGrid pitch internally. Target printer: [A1 or A1 Mini].

Prefer reusing existing geometry and interfaces. Expose useful parameters and export editable STEP plus printable STL. Use the official native snap or openConnect modeling geometry for all mating components, record provenance and license, and do not claim fit until printed and physically verified. Separate structural joints from removable accessory mounts. Include software geometry checks, slicer-fit verification, a minimal test coupon if mating tolerances change, and a manual test checklist. Update the catalog and docs with exact changes, assumptions, evidence, and unresolved issues. Keep the implementation simple.
```
