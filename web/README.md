# openGrid Studio (GitHub Pages)

React + TypeScript + Vite + React Three Fiber (Three.js) + Drei + Tailwind CSS + Radix primitives. All CAD geometry comes from the parent repository's verified Python/OpenSCAD generation pipeline.

## Development

From the repository root, generate CAD first (or use the downloaded Actions artifact), then:

```bash
python scripts/build_site_assets.py
cd web
npm install
npm run dev
```

The public `web/public/assets/` catalog, GLBs, previews and source downloads are generated from validated CAD outputs. They're intentionally excluded from source control. Always rebuild assets when CAD source changes.

## GitHub Pages

The Vite project has the repository-specific base path `/opengrid-cad-library/`. The GitHub Actions pipeline prepares assets, builds the site and runs static smoke checks, then uses official GitHub Pages actions for deployment. Enable **Settings → Pages → Build and deployment → GitHub Actions** in the repository settings to authorize publication.

## Verification boundaries

The catalog's `cadValid` and `meshWatertight` flags come from the actual Python pipeline. `fitVerified`, `loadTested`, and `slicerVerified` remain false until corresponding tests have been performed. Parameter controls for the cable hook generate a **build request JSON**, and the displayed model remains the last CAD-validated geometry. A user can run the existing GitHub Actions workflow with matching parameter inputs to generate a new artifact. No browser-embedded CAD generation or printer control is implied.

All models and sources are public because the repository is public.

## CAD preview fidelity

The studio includes 10 source-generated CAD parts, including bare Full/Lite directional modeling snaps and separate openConnect-headed snaps. Viewer contour lines and neutral matte materials are a visualization aid only. The exported GLB is checked against the source mesh for triangle count, physical bounds, and volume; original CAD files remain available under Files. Publisher-derived parametric geometry and independently designed prototypes are labeled separately. Real slicer and fit testing are still pending.

## Official openGrid boards

Four original David D Full/Lite board files (2×2 and 4×4) are now in the **Boards** category. Their 3MF sources are imported unchanged from the Printables publisher listing, with pinned SHA-256 hashes, file IDs, source URLs, and CC BY 4.0 attribution in `vendor/davidd-opengrid/manifest.json`. The same models are converted to independent, validated GLB previews. Three original STEP files are included; Full 4×4 STEP can be obtained on the publisher's listing. The simple pitch coupon remains clearly categorized as a **Prototype**, and must never stand in for the original board.

## Original published accessories

Six first-party David D models are now included: Minimal Hook, Full/Lite Wall Mount, Color Cover Snap, Multiconnect Directional Snap v2, and M3 Nut Snap. Each has original 3MF + STEP and a checked source-file manifest under `vendor/davidd-opengrid/accessories-manifest.json`. They retain publisher license/attribution, and fit/load remain unverified. Gridfinity shelves are excluded due to their separate noncommercial license.
