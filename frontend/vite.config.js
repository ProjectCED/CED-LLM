import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_BACKEND_URL || 'http://localhost:5000',
        rewrite: (path) => path.replace(/^\/api/, ''), // Remove `/api` prefix
      },
    },
    port: process.env.VITE_PORT || 5173,
  },
})
