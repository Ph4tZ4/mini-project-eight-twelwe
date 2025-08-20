// config/api.js
export const API_CONFIG = {
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://your-production-api.com' 
    : 'http://localhost:5050',
  endpoints: {
    login: '/api/login',
    register: '/api/register',
    profile: '/api/profile'
  }
}
