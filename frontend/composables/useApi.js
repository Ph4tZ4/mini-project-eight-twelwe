// composables/useApi.js
export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase || 'http://localhost:5550'
  const { getItem } = useLocalStorage()

  const getAuthHeaders = () => {
    // Try to get token from cookie first (for admin system)
    const tokenCookie = useCookie('auth-token')
    if (tokenCookie.value) {
      return { 'Authorization': `Bearer ${tokenCookie.value}` }
    }
    
    // Fallback to localStorage (for regular user system)
    const token = getItem('token')
    return token ? { 'Authorization': `Bearer ${token}` } : {}
  }

  const apiCall = async (endpoint, options = {}) => {
    const url = `${baseURL}${endpoint}`
    
    try {
      const response = await $fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
          ...options.headers
        }
      })
      return response
    } catch (error) {
      console.error('API Error:', error)
      
      // Handle authentication errors
      if (error.status === 401) {
        // Clear invalid token and redirect appropriately
        const tokenCookie = useCookie('auth-token')
        const userCookie = useCookie('auth-user')
        
        if (tokenCookie.value || userCookie.value) {
          // Admin session expired
          tokenCookie.value = null
          userCookie.value = null
          navigateTo('/admin/login')
        } else {
          // Regular user session expired
          const { removeItem } = useLocalStorage()
          removeItem('token')
          removeItem('user')
          navigateTo('/login')
        }
      }
      
      throw error
    }
  }

  const isAuthenticated = () => {
    const { getItem } = useLocalStorage()
    const token = getItem('token')
    const user = getItem('user')
    return !!(token && user)
  }

  const getCurrentUser = () => {
    const { getItem } = useLocalStorage()
    return getItem('user')
  }

  const logout = () => {
    const { removeItem } = useLocalStorage()
    removeItem('token')
    removeItem('user')
    navigateTo('/login')
  }

  return {
    apiCall,
    baseURL,
    getAuthHeaders,
    isAuthenticated,
    getCurrentUser,
    logout
  }
}
