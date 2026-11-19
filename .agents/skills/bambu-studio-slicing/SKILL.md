---
name: bambu-studio-slicing
description: Prepare and verify 3D print jobs using official Bambu Studio profiles and supported command-line slicing. Use when a Bambu A1 or A1 Mini STL/3MF needs orientation, supports, print estimates, or slicer preflight.
---

# Bambu Studio slicing workflow

Official references: `https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage` and `https://github.com/bambulab/BambuStudio`.

Bambu Studio is the **default** slicer for the Bambu printer. Follow actual installed version's documented CLI. It uses printer, filament, and process profiles; never invent profile names, quality metrics, filament mass, estimated time, or G-code.

1. Verify the installed Bambu Studio executable, version, printer profile (A1/A1 Mini), nozzle, material, bed settings, and local file existence.
2. Load a valid STL/3MF and check dimensions in inches, volume, orientation, support needs and interference.
3. Slice using the actual available CLI/GUI. Record settings, warnings, time, supports, and real filament mass in pounds from the slicer output.
4. Inspect toolpaths/layers and ensure no model extends outside the build plate.
5. Export 3MF or sliced format for the user's review; print start requires explicit confirmation and a connected, properly configured printer.
6. Record real outcomes after printing; do not mark `fit_verified` from slicer success alone.

An AI skill is guidance only. If Bambu Studio is not installed or the agent has no execution tools, explain that slicing cannot be performed yet. Never use third-party printer-control packages without separate review/approval.

For a community alternative, review `https://github.com/heyixuan2/bambu-studio-ai` (independent, **not** an official Bambu Lab skill) before any deployment.
