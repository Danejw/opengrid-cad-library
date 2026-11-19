---
name: fusion-mcp
description: Use official Autodesk Fusion MCP for live desktop CAD or optional Fusion Compute MCP cloud sessions. Apply when an agent must inspect or modify native Fusion parametric sketches, features, constraints, joints, assemblies, and exports through an available, authenticated MCP connection.
---

# Fusion MCP engineering

Prefer portable CadQuery/source-controlled STEP+STL for simple repeatable parts. Choose Fusion when native Fusion feature history, sketch constraints, assembly joints, or interactive design review materially helps.

## Select backend

1. **Fusion desktop MCP** (official): requires Fusion installed and open on the *same machine* as the agent client, and Fusion MCP enabled in Preferences > General > API. Default local URL: `http://127.0.0.1:27182/mcp`. For Cursor use a Streamable HTTP MCP configuration. Before work, list available tools and inspect the active design. Read `references/fusion-setup.md`.
2. **Fusion Compute MCP** (official public beta): optional cloud backend `https://developer.api.autodesk.com/da/v3/mcp/fusion`. Requires Autodesk account, active Fusion license, and Fusion Team hub. Sessions have changing availability/limits. Save/export before session expiration. Verify subscription/access first.
3. **Fusion Data MCP**: primarily navigate Fusion project data/hubs/metadata; do not confuse it with geometry editing.

When the MCP tool is unavailable, **do not claim it ran**. Continue using the source-controlled parametric CAD backend or state the missing connection.

## Process

Read `AGENTS.md`, `docs/MCP_INTEGRATIONS.md`, and `docs/INTERFACES.md`. Read-only inspect first, make changes in a new named design/feature version unless in-place editing is explicitly requested, generate or modify constraints through actual Fusion tools, inspect changed feature history and interference, export STEP/STL, and compare geometry with requirements. Respect native openGrid connector sources and their licenses.

A tool returning success does not prove the physical part functions. Keep software validation and real physical evidence separate.

## Security and costs

Use localhost or Autodesk's documented official cloud endpoint. Never commit Autodesk credentials, tokens, local hub metadata, or proprietary designs without permission. Before performing manufacturing actions or paid/cloud work, verify permissions and user intent. No unrequested printer starts.
