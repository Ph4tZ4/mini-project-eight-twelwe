export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ['~/css/main.css'],
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:5050'
    }
  },
  devServer: {
    port: 3030
  },
  // แก้ไข hydration issues
  ssr: true,
  nitro: {
    preset: 'node'
  },
  experimental: {
    payloadExtraction: false
  }
});