import { defineConfig } from 'vite'; import react from '@vitejs/plugin-react';

// The app normally calls http://localhost:8000 directly. The proxy also makes
// relative /api requests work during development without a CORS preflight.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true, proxy: { '/api': 'http://localhost:8000' } },
});
