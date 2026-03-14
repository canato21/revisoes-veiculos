import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'all',
      '.ngrok-free.app',
      '.ngrok-free.dev',
      'unadventuring-braiden-preauricular.ngrok-free.dev'
    ]
  }
})