import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
