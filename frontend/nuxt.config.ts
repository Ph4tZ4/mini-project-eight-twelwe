export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },
  
  // CSS processing
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  

  
  runtimeConfig: {
    public: {
      apiBase: process.env.VITE_API_URL || 'http://localhost:5550'
    }
  },
  
  devServer: {
    port: 3330
  },
  
  // Production configuration
  ssr: true,
  
  nitro: {
    preset: 'node-server',
    host: '0.0.0.0',
    port: 3000
  },
  
  // Fix hydration issues
  experimental: {
    payloadExtraction: false
  },
  
  // Hydration configuration
  ssr: true,
  spaLoadingTemplate: false,
  
  // Vue configuration for hydration
  vue: {
    config: {
      hydrationMismatchDetails: false
    }
  },
  
  // Better hydration handling
  router: {
    options: {
      scrollBehaviorType: 'smooth'
    }
  },
  
  // App configuration
  app: {
    head: {
      viewport: 'width=device-width,initial-scale=1',
      charset: 'utf-8'
    }
  }
});