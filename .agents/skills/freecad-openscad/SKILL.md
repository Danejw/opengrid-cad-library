---
name: freecad-openscad
description: Select and operate FreeCAD or OpenSCAD for portable parametric CAD and modifying open-source printable designs when an installed tool or command-line environment is available.
---

# FreeCAD and OpenSCAD

These are useful **optional** editing and source-driven modeling backends. Verify each program exists and inspect its supported scripting/CLI version before running anything. Do not imply an MCP connection exists solely because this skill is installed.

- **FreeCAD:** graphical editing, feature-based CAD, Python macros, STEP import/export; source: https://www.freecad.org/ and https://wiki.freecad.org/
- **OpenSCAD:** deterministic CSG models and parametric 3D-print community design sources; source: https://openscad.org/documentation.html
- **CadQuery:** preferred initial project source for automated parts; retain source-controlled Python.

For imported openGrid models, preserve original snap geometry and licensing. STEP is generally useful for cross-CAD BRep interchange, STL for slicing, and native editable source for reproducibility. Avoid editing meshes as if they retained parametric CAD history.

When exporting or editing a model, check unit scaling, coordinate origin, shape validity, watertightness, feature placement, and generated file provenance. Run tools only when installed and accessible; never fabricate tool execution or output.
