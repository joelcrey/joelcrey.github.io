import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: '/arabic-reader/',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Arabic Reading Assistant',
        short_name: 'Arabic Reader',
        description: 'Interactive Arabic text reader with word analysis',
        theme_color: '#ffffff',
        background_color: '#f9f8f5',
        display: 'standalone',
        icons: [
          { src: 'icon.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' }
        ]
      }
    })
  ]
})