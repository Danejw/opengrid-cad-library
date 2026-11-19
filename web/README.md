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
