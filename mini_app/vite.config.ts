import { defineConfig } from 'vite';

export default defineConfig({
  base: './', // Use relative paths so it can be deployed on GitHub Pages easily
  server: {
    port: 5173,
    host: true
  }
});
