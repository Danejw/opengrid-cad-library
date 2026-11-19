# How agents choose expert skills

`AGENTS.md` is the root policy. Read a skill when the current task requires its domain. Skills provide **instructions and optional scripts**, not automatic installation of their target software.

| Task | Primary skill | Complementary skill |
|---|---|---|
| New part from prompt | `parametric-part-cad` | `parametric-3d-printing`, `mesh-validation` |
| Add genuine openGrid connector | `opengrid-interface-engineering` | `tolerance-stackup`, `dfm-review` |
| Optimize support and printability | `agentscad-fdm-dfam` | `bambu-studio-slicing` |
| Design linkage or moving assembly | `linkage-synthesis` | `machine-element-sizing`, `tolerance-stackup` |
| Calculate allowable elements | `machine-element-sizing` | `design-review-package` |
| Analyze clearance and fitting | `tolerance-stackup` | `opengrid-interface-engineering` |
| CAD design review and risks | `dfm-review` | `design-review-package` |
| Work in Fusion desktop/cloud | `fusion-mcp` | `parametric-part-cad` |
| Edit FreeCAD/OpenSCAD file | `freecad-openscad` | `mesh-validation` |
| Slice with Bambu Studio | `bambu-studio-slicing` | `mesh-validation` |
| Control OrcaSlicer via connected MCP | `orcaslicer-mcp-skills` | `mesh-validation` |
| Create a new reusable skill | `skill-creator` | `opengrid-interface-engineering` if an interface skill |

Avoid loading every skill simultaneously. Start with the smallest relevant set and add others when the task genuinely requires them. Validate tool availability instead of inventing results.

## Standard output states

`draft` → `cad_valid` → `slicer_verified` → `fit_verified` → `load_tested`.

These are evidence categories rather than an automatically guaranteed sequence. Missing physical evidence means no physical-fit claim.
