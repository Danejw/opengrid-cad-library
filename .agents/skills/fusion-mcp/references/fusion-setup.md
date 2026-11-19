# Official Autodesk Fusion MCP setup

Official docs:
- https://github.com/Autodesk/ai-integrations/tree/main/fusion/local-mcp-server
- https://help.autodesk.com/view/fusion360/ENU/?guid=FMCP-OVERVIEW
- https://help.autodesk.com/cloudhelp/ENU/ADSKMCP-FusionDesktopMcp/files/ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html.html
- https://www.autodesk.com/products/fusion-360/blog/fusion-compute-mcp/

## Desktop on Windows and Cursor

1. Install and open Autodesk Fusion.
2. Enable `Preferences > General > API > Fusion MCP Server`.
3. Confirm the displayed port. Default: `http://127.0.0.1:27182/mcp`.
4. Add `autodesk-fusion` as a Streamable HTTP server in Cursor's MCP settings, or see `config/mcp.cursor.example.json`.
5. Verify Fusion and Cursor are running on **the same Windows machine**. Open an expendable test document, list tools, then create a tiny test part.

If the client operates in a cloud computer, its localhost URL points to the **cloud computer**, not your Windows PC. Connect to Autodesk Compute MCP through an authorized cloud client, or run a local agent/client with desktop Fusion. Do not expose the unauthenticated local Fusion MCP port publicly.

## Fusion Compute MCP public beta

Documented official cloud endpoint: `https://developer.api.autodesk.com/da/v3/mcp/fusion`.

As of September 2026: requires Autodesk account + active Fusion license + Fusion Team hub, with two concurrent sessions, 1-hour max session and 15-minute idle timeout (limits may change). Confirm your account has access. This is optional and may entail subscription requirements; no credentials belong in Git.

## Backend split

- CAD code + Git: reproducible parametric source of truth.
- Fusion local/compute: interactively inspect and refine native feature-history models.
- Slicer: verify actual printable geometry, support strategy and consumption.
- Physical print: evidence of fit and function.
