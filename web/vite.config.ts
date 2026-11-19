import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/opengrid-cad-library/',
  build: { outDir: 'dist', assetsInlineLimit: 0, sourcemap: false },
  server: { host: true, port: 5173 },
});
