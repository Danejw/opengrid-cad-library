# Parametric 3D Printing — AI Skill for CadQuery

An AI skill that enables AI agents (Claude Code, Kiro, Amazon Q Developer, etc.) to design parametric 3D models for FDM 3D printing using [CadQuery](https://cadquery.readthedocs.io/) (Python).

## What is this?

This is a **skill** — a structured set of instructions, references, and utility scripts that an AI agent can use to become proficient at designing 3D-printable objects. When loaded, the agent gains:

- Knowledge of FDM print constraints (wall thickness, overhangs, tolerances)
- A phased workflow with progressive preview and user feedback
- CadQuery best practices (BRep thinking, selector patterns, Free Function API)
- Utility scripts for preview rendering, mesh validation, and STL/3MF export
- Gridfinity bin generation support
- A design review checklist to catch issues before printing

## Why?

Designing 3D models from scratch is time-consuming. With this skill, you can describe what you need in plain language — "a wall-mounted holder for my Raspberry Pi 4" — and the AI agent will:

1. Ask the right questions (dimensions, mounting method, material)
2. Build the model incrementally with previews at each phase
3. Apply print-friendly design rules automatically
4. Export a ready-to-slice STL file with print recommendations

## Skill Structure

```
SKILL.md                        # Main skill definition (auto-loaded by agents)
references/
  cadquery-advanced.md          # CadQuery selectors, patterns, Free Function API
  design-review.md              # Pre-delivery design review checklist
  gridfinity.md                 # Gridfinity spec & API reference
  preview-workflow.md           # Progressive preview loop details
  print-rules.md               # FDM design rules & common pitfalls
  utility-scripts.md            # Script usage documentation
scripts/
  run_cadquery_model.py         # Execute model + render preview + JSON output
  preview.py                    # STL → multi-view PNG rendering
  gridfinity.py                 # Gridfinity bin generator module
  mesh_io.py                    # STL loading & watertight validation
  stl_to_3mf.py                # STL → 3MF converter
  outline_from_scan.py          # Photo/scan → pocket outline extraction
```

## Usage

### With Kiro

Place this skill in your project's `.kiro/skills/` directory:

```bash
mkdir -p .kiro/skills
cp -r parametric-3d-printing .kiro/skills/
```

Kiro will automatically activate the skill when you mention 3D printing, STL, CadQuery, or describe a physical object to manufacture.

### With Claude Code

Add this as a skill or include the `SKILL.md` content in your project instructions. Claude Code will follow the phased workflow and use the utility scripts.

### Prerequisites

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install cadquery>=2.6.1 trimesh>=4.0 pyrender>=0.1.45 Pillow>=10 numpy>=1.24 lxml>=4.9
```

> Requires Python 3.10–3.12 (OCC kernel lacks 3.13+ wheels).  
> Alternative: `conda install -c cadquery -c conda-forge cadquery`

## Credits & Inspiration

This skill was built upon ideas and approaches from:

- **[flowful-ai/cad-skill](https://github.com/flowful-ai/cad-skill)** — AI skill for CAD model generation, providing the structural foundation for how an AI agent should approach 3D modeling tasks.
- **[jmwright/cadquery-llm-skill](https://github.com/jmwright/cadquery-llm-skill)** — CadQuery-specific LLM skill with detailed CadQuery patterns, best practices, and common pitfalls that informed the technical reference material.

## License

MIT
