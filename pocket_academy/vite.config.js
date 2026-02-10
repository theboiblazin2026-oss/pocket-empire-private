import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Fix for Vercel blank page
  server: {
    host: true, // Exposes the server to the local network
  }
})
