// plugins/client-only.client.js
// This plugin runs only on the client side to handle hydration safely

export default defineNuxtPlugin(() => {
  // Ensure client-side only features are properly initialized
  if (process.client) {
    // Initialize any client-side only functionality here
    console.log('Client-side hydration complete')
    
    // Check for corrupted localStorage data and clean it up
    try {
      const token = localStorage.getItem('token')
      if (token && token.startsWith('eyJ')) {
        // Token looks like JWT, verify it's not wrapped in JSON
        try {
          JSON.parse(token)
          // If parsing succeeded, the token was incorrectly stored as JSON
          console.log('Fixing localStorage token format')
          localStorage.setItem('token', token.replace(/"/g, ''))
        } catch (e) {
          // Token is correctly stored as string, no action needed
        }
      }
      
      const user = localStorage.getItem('user')
      if (user && !user.startsWith('{')) {
        // User data doesn't look like JSON, might be corrupted
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        console.log('Cleared corrupted user data')
      }
    } catch (error) {
      console.log('Error checking localStorage, clearing...')
      localStorage.clear()
    }
    
    // Remove hydration mismatch warnings in development
    if (process.dev) {
      const originalError = console.error
      console.error = (...args) => {
        if (typeof args[0] === 'string' && args[0].includes('Hydration')) {
          return // Suppress hydration warnings in development
        }
        originalError.apply(console, args)
      }
    }
  }
})
