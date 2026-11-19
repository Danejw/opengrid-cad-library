# MCP and engineering software integration architecture

## Intended system

```text
Human / AI request
  -> AGENTS.md + task-specific .agents/skills/<name>/SKILL.md
  -> discover available tools and authenticate/authorize
  -> choose CAD backend
       CadQuery source code (default, works without MCP)
       Fusion Desktop MCP (optional, local Windows)
       Fusion Compute MCP (optional Autodesk cloud)
       FreeCAD / OpenSCAD (optional native software)
  -> verify BRep / mesh and assembly clearance
  -> choose slicer
       Bambu Studio CLI / GUI (default)
       OrcaSlicer MCP (optional, if connected)
  -> inspect slicer output -> explicit human approval -> optional print
  -> record physical results -> promote verified parts
```

## Preferred software and why

| Work | Default | Alternate / MCP | Requirement |
|---|---|---|---|
| Repeatable parametric parts | CadQuery in `cad/` | Fusion local/compute, FreeCAD, OpenSCAD | Python CAD dependencies; local CAD program only when selected |
| Native constrained designs and assemblies | Fusion Desktop MCP | Fusion Compute MCP | Installed Fusion + enabled local server, or eligible Autodesk cloud account |
| Editing official 3D printing OpenSCAD designs | OpenSCAD | CadQuery reimplementation where license permits | Local OpenSCAD installed |
| Slicing Bambu A1 / A1 Mini models | Bambu Studio | OrcaSlicer MCP | Installed slicer and correct printer/material profile |
| Test reports | source-backed CAD + slicer output | Physical measurements | Real printed part for fit and load assertions |

## Official Autodesk Fusion desktop MCP

**Official reference:** https://github.com/Autodesk/ai-integrations/tree/main/fusion/local-mcp-server

Autodesk documents a native MCP server in Fusion. On your **Windows PC**, install/open Fusion, go to Preferences > General > API, enable Fusion MCP Server, and confirm the displayed local endpoint (default `http://127.0.0.1:27182/mcp`). Cursor can connect through Streamable HTTP via its MCP settings. Starter example: `config/mcp.cursor.example.json`.

**Critical limitation:** `127.0.0.1` resolves to the machine running the MCP client. If the agent runs in a cloud environment, the local Fusion server on your PC is *not* reachable merely by using the URL. Use a local Cursor/agent environment for native desktop control. Never expose the unauthenticated loopback endpoint on the public Internet.

**Verified source:** https://help.autodesk.com/cloudhelp/ENU/ADSKMCP-FusionDesktopMcp/files/ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html.html

## Autodesk Fusion Compute MCP (public beta)

Official endpoint: `https://developer.api.autodesk.com/da/v3/mcp/fusion`.

As documented September 2026: Autodesk account, an active Fusion license, Fusion Team hub, and an OAuth-capable MCP client. Supports cloud-native CAD, assembly, documents/exports and manufacturing without occupying the desktop. Reported beta limits: 2 concurrent sessions, 1-hour max, 15-minute idle timeout, queueing when capacity is full. **Must save or export before sessions expire.** Access, licensing and limits must be rechecked when setting up. No automatic cloud use or incurred charges.

Autodesk source: https://www.autodesk.com/products/fusion-360/blog/fusion-compute-mcp/

## Fusion Data MCP

Cloud data/project management for Fusion hubs, folders, items. It is distinct from geometry-editing local or Compute MCP. Docs: https://help.autodesk.com/view/fusion360/ENU/?guid=FMCP-OVERVIEW

## OrcaSlicer MCP

Official skill source: https://github.com/OrcaSlicer/orcaslicer-mcp-skills

The vendored skill in `.agents/skills/orcaslicer-mcp-skills` is separate from the **actual application server**. Install a compatible official OrcaSlicer version, enable its MCP server in Preferences > General > AI features, and add it to the agent client. Agent can operate only after the server is running and connected; verify available tool list dynamically. Source: https://github.com/OrcaSlicer/orcaslicer-mcp-skills/blob/main/README.md.

## Bambu Studio

Default path: `https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage`. The project-specific Bambu Studio skill teaches the official CLI and review gates; it does not make Bambu Studio installed or connected. A community option `https://github.com/heyixuan2/bambu-studio-ai` is **independent, not Bambu Lab-official**, and is optional, subject to separate security/dependency review.

## Tool discovery and execution

Always identify whether a backend is **available**, **configured**, **authorized**, and **verified in this session** before acting. Tool absence means use a different backend or report a clear blocker. Never fake a live Fusion or Orca action from static instructions.

Before external side effects, prefer read-only discovery. Ask approval before machine movement/print start, irreversible changes, publishing private data, or paid Fusion/cloud sessions. Keep secrets outside the repository; track artifacts and provenance. No headless printer access until the user explicitly authorizes a specific print.

## Testing the whole pipeline

1. CadQuery: run unit tests, generate STEP/STL.
2. Mesh: validate solid/mesh and printer dimensions.
3. Fusion: when explicitly connected, create a small test design and read it back; compare output to source.
4. Slicer: slice a sample with the actual printer + filament profile; inspect the returned mass/time/toolpath warnings.
5. Printing: only after approval; record real fit and print evidence.
6. Promote reusable connectors only after physical evidence in `opengrid-interface-engineering`.
