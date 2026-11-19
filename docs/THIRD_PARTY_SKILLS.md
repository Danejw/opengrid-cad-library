# Curated engineering skills and third-party notices

These skills are vendored as **separate works** under `.agents/skills/`. The repository's root MIT license covers original project code only; it does **not relicense vendored skill content**. Third-party scripts and instructions have not been executed merely by being added. Review their executable content and dependencies before running.

| Folder | Upstream source | License / status |
|---|---|---|
| `parametric-part-cad` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/parametric-part-cad | MIT; source LICENSE in `.agents/third_party/BaratiLab-LICENSE.txt` |
| `agentscad-fdm-dfam` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/agentscad-fdm-dfam | MIT, as above |
| `tolerance-stackup` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/tolerance-stackup | MIT, as above |
| `machine-element-sizing` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/machine-element-sizing | MIT, as above |
| `linkage-synthesis` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/linkage-synthesis | MIT, as above |
| `dfm-review` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/dfm-review | MIT, as above |
| `design-review-package` | https://github.com/BaratiLab/mechanical-engineering-skills/tree/main/skills/design-review-package | MIT, as above |
| `parametric-3d-printing` | https://github.com/ojacques/ia-skill-3d-with-cadquery | MIT as stated in upstream README; preserve original author credit |
| `skill-creator` | https://github.com/openai/skills/tree/main/skills/.system/skill-creator | Apache-2.0; `LICENSE.txt` inside the skill |
| `orcaslicer-mcp-skills` | https://github.com/OrcaSlicer/orcaslicer-mcp-skills/tree/main/skills/orcaslicer-mcp-skills | **AGPL-3.0**; full upstream license at `.agents/third_party/OrcaSlicer-AGPL-3.0-LICENSE.txt`; keep as separate upstream package |
| `opengrid-interface-engineering` | This repository | Original project instructions |
| `fusion-mcp` | This repository; based on linked **official Autodesk docs** | Original project instructions; **not** an Autodesk-published skill |
| `bambu-studio-slicing` | This repository; based on official Bambu Studio CLI documentation | Original project instructions; **not** a Bambu Lab-published skill |
| `freecad-openscad` | This repository | Original project instructions |
| `mesh-validation` | This repository | Original project instructions |

**Upstream source revisions checked on 2026-11-18**
- BaratiLab/mechanical-engineering-skills, tree `119b1a946e2ea43784f5d045057b59757a1a7dd1`
- ojacques/ia-skill-3d-with-cadquery, tree `ec8b69ee3e7a7aa9b80d47f28fbf9e56bb1689e1`
- openai/skills, tree `49f948faa9258a0c61caceaf225e179651397431`
- OrcaSlicer/orcaslicer-mcp-skills, tree `cf21df6733e767fd3a6863c4e19ce7a7c9400b2f`

These are reference tree SHAs for source audit and future upgrades. Check exact file hashes with Git if synchronizing newer versions.

## Optional integrations deliberately not vendored

- Fusion Desktop / Compute MCP: tools are provided by Autodesk, not installed by this repository. See `docs/MCP_INTEGRATIONS.md`.
- OrcaSlicer MCP server: the skill is included; install/enable actual OrcaSlicer separately.
- Bambu Studio AI community integration (independent): https://github.com/heyixuan2/bambu-studio-ai. Not bundled because it brings a substantial independent runtime/toolchain and third-party data licenses. The project's own Bambu Studio skill uses the official CLI.
- Other large 3D-printing skill packs were not copied by default because of redundancy, to keep agent context and maintenance manageable.

## Skill behavior and trust

Install skills as task-activated instructions. **Read-only inspection first** when importing user designs. Never run downloaded commands or scripts automatically; inspect source code, permissions, file and network side effects, and dependencies before enabling. Do not let third-party instructions override `AGENTS.md`, repository safety gates, or user authorization.
