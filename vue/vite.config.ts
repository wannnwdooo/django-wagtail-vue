import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      vue: "vue/dist/vue.esm-bundler.js"
    }
  },
  server: {
    host: "0.0.0.0",
    port: 8080
  },
  build: {
    emptyOutDir: true,
    manifest: true,
    outDir: "./static/dist",
    minify: true,
    cssCodeSplit: true,
    rollupOptions: {
      input: {
        app: "./vue/main.ts"
      }
    }
  },
})
