export default defineNuxtRouteMiddleware((to, from) => {
  // Check if running on client side
  if (process.client) {
    const token = useCookie('auth-token')
    const user = useCookie('auth-user')

    // If user is already logged in, redirect appropriately
    if (token.value && user.value) {
      // If user is admin and trying to access admin login, redirect to admin dashboard
      if (to.path === '/admin/login' && user.value.is_admin) {
        return navigateTo('/admin/dashboard')
      }
      
      // If regular user trying to access regular login, redirect to home
      if (to.path === '/login' && !user.value.is_admin) {
        return navigateTo('/')
      }
    }
  }
})
