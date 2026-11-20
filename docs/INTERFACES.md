# Native connector contract

## Verified dimensional facts

Official openGrid uses a 28 mm cell-to-cell pitch, about **1.1024 inches**. Lite panels are **4 mm (0.157 in)** thick and Full panels are **6.8 mm (0.268 in)** thick. The documented default is a full board mounted through separate snaps and a Lite board with integrated screw holes. Bare Lite snaps can use approximately 3.4 mm of panel depth, so the original author says a Lite snap can be used with Full and Lite panels. These are **reference dimensions** and do not, by themselves, describe a functional snap.

Sources:
- https://www.opengrid.world/guides/quickstart/
- https://www.opengrid.world/guides/modeling/
- https://www.opengrid.world/guides/snaps/

## Native modules to depend on, rather than recreating

- **Official bare snaps:** normal, directional, lock snap, Full and Lite variants; modeling files at https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem
- **openConnect:** snap + threaded heads and corresponding negative slots; modeling source: https://github.com/mitufy/opengrid-projects/tree/main/lib ; model listing https://www.printables.com/model/1559478-openconnect-opengrids-own-connector-system
- **Multiconnect:** use exact negative modeling geometry for a receiving channel: https://www.opengrid.world/guides/modeling/
- **Underware:** openGrid-based cable channels: https://www.opengrid.world/guides/quickstart/underware/

**Never treat this package's sample square windows, bolt holes, or 28 mm centering pattern as genuine snap slots.** They are templates for objects and mounting points only.

## Recommended way to make a genuine custom accessory

1. Download the latest applicable upstream **bare snap** CAD file (STEP, 3MF, SCAD, or editable model). Record its source URL, license, and version.
2. Open the sample `adapter_blank.step` or `grid_tray.step` in Fusion 360 or CADQuery.
3. Bring in the **source model** for an appropriate Lite or Full snap, or add a verified upstream openConnect slot cutout to the accessory's back. Position at the 28 mm grid cell centers.
4. Ensure a manufacturable connection with adequate solid material between the native snap and the object, and select print orientation to protect latch strength.
5. Print a 2-cell test piece and physically check insertion, retention, removal, and repeatability on a real openGrid panel.
6. Only after that check, mark the interface as `fit_verified` and re-use it for new accessories.

A Lite snap is not automatically strong enough for every load. For multi-point or load-bearing attachments, use an appropriate connector and test the assembly. Do not use openGrid snaps to carry furniture, overhead/loft loads, or other safety-critical structures.

## Suggested verification record

```json
{
  "interface_id": "opengrid-lite-directional-snap-v1",
  "source_url": "https://www.opengrid.world/guides/modeling/",
  "upstream_file": "REPLACE_AFTER_DOWNLOAD",
  "upstream_version_or_sha": "REPLACE_AFTER_DOWNLOAD",
  "license": "CHECK_UPSTREAM",
  "printer": "Bambu A1",
  "material": "PLA or PETG (record actual)",
  "slicer_profile": "RECORD",
  "fit_verified": false,
  "load_approved_lbs": null,
  "notes": "Use actual printed test to verify"
}
```

## Studio snap variants and geometry fidelity

The Studio publishes two **bare directional modeling snaps** (Full 6.8 mm, Lite 3.4 mm snap in the 4 mm board) plus two separate **openConnect-headed directional snaps** (Full 6.8 mm, Lite 4 mm) from the repository's pinned, unchanged `mitufy/opengrid-projects` OpenSCAD generator. These are distinct mechanical parts with distinct names and downloadable source-generated 3MF files.

The source is attributed under CC BY 4.0 in `vendor/mitufy-opengrid/ATTRIBUTION.md`. The bare versions are intended as native modeling foundations, and should not be presented as verified printable finished mounting hardware. The Studio GLB models are created directly from verified watertight meshes, with bounding-box, face-count, and volume round-trip checks. Visual edge lines and shading do not change the downloaded geometry.

These variants follow upstream published snap dimensions and concepts; they have not been dimensionally compared against every separately distributed David D official STL release. Actual printed insertion, retention, and load capacity remain unverified.
