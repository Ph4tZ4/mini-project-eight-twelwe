// utils/storage.js
// Safe localStorage wrapper for SSR compatibility

export const useLocalStorage = () => {
  const setItem = (key, value) => {
    if (process.client) {
      try {
        // If value is already a string, save it directly
        // Otherwise JSON.stringify it
        const stringValue = typeof value === 'string' ? value : JSON.stringify(value)
        localStorage.setItem(key, stringValue)
      } catch (error) {
        console.error('Failed to save to localStorage:', error)
      }
    }
  }

  const getItem = (key, defaultValue = null) => {
    if (!process.client) return defaultValue
    
    try {
      const item = localStorage.getItem(key)
      if (!item) return defaultValue
      
      // Try to parse as JSON first, if it fails return as string
      try {
        return JSON.parse(item)
      } catch (parseError) {
        // If JSON parsing fails, return the raw string (for tokens)
        return item
      }
    } catch (error) {
      console.error('Failed to read from localStorage:', error)
      return defaultValue
    }
  }

  const removeItem = (key) => {
    if (process.client) {
      try {
        localStorage.removeItem(key)
      } catch (error) {
        console.error('Failed to remove from localStorage:', error)
      }
    }
  }

  const clear = () => {
    if (process.client) {
      try {
        localStorage.clear()
      } catch (error) {
        console.error('Failed to clear localStorage:', error)
      }
    }
  }

  return {
    setItem,
    getItem,
    removeItem,
    clear
  }
}
