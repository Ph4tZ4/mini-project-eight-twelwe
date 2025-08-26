export default defineNuxtRouteMiddleware((to, from) => {
  // Check if running on client side
  if (process.client) {
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    
    // If no token or user, redirect to login
    if (!token || !user) {
      return navigateTo('/login')
    }
    
    // Optional: Validate token format or expiration here
    try {
      JSON.parse(user) // Validate user data format
    } catch (error) {
      // Invalid user data, clear and redirect
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      return navigateTo('/login')
    }
  }
})
