export default defineNuxtRouteMiddleware((to, from) => {
  // Check if running on client side
  if (process.client) {
    const token = useCookie('auth-token')
    const user = useCookie('auth-user')

    // Check if user is logged in
    if (!token.value || !user.value) {
      return navigateTo('/admin/login')
    }

    // Check if user is admin
    if (!user.value.is_admin) {
      // Redirect non-admin users to regular login
      throw createError({
        statusCode: 403,
        statusMessage: 'Admin access required'
      })
    }
  }
})
