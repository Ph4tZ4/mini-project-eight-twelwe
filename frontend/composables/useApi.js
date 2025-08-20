// composables/useApi.js
export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase || 'http://localhost:5050'

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token')
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
        // Clear invalid token and redirect to login
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        navigateTo('/login')
      }
      
      throw error
    }
  }

  const isAuthenticated = () => {
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    return !!(token && user)
  }

  const getCurrentUser = () => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
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
