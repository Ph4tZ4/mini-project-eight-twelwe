// composables/useCart.js
export const useCart = () => {
  const { apiCall, isAuthenticated } = useApi()

  const items = useState('cart_items', () => [])
  const totals = useState('cart_totals', () => ({ subtotal: 0, total_quantity: 0 }))
  const loading = useState('cart_loading', () => false)
  const cartCount = useState('cart_count', () => 0)

  const fetchCart = async () => {
    if (!isAuthenticated()) {
      items.value = []
      totals.value = { subtotal: 0, total_quantity: 0 }
      cartCount.value = 0
      return
    }
    loading.value = true
    try {
      const res = await apiCall('/api/cart', { method: 'GET' })
      if (res.success) {
        items.value = res.cart.items || []
        totals.value = res.cart.totals || { subtotal: 0, total_quantity: 0 }
        cartCount.value = totals.value.total_quantity
      }
    } catch (error) {
      console.error('Error fetching cart:', error)
      items.value = []
      totals.value = { subtotal: 0, total_quantity: 0 }
      cartCount.value = 0
    } finally {
      loading.value = false
    }
  }

  const addItem = async (productId, quantity = 1) => {
    if (!isAuthenticated()) {
      // For non-authenticated users, you could implement local storage cart
      throw new Error('Please login to add items to cart')
    }

    try {
      const res = await apiCall('/api/cart/add', {
        method: 'POST',
        body: { product_id: productId, quantity }
      })
      if (res.success) {
        await fetchCart()
        // Show success notification
        return { success: true, message: res.message || 'Item added to cart' }
      }
      return res
    } catch (error) {
      console.error('Error adding item to cart:', error)
      return { success: false, message: 'Failed to add item to cart' }
    }
  }

  const updateItem = async (productId, quantity) => {
    if (!isAuthenticated()) {
      throw new Error('Please login to update cart')
    }

    if (quantity <= 0) {
      return removeItem(productId)
    }

    try {
      const res = await apiCall('/api/cart/update', {
        method: 'PUT',
        body: { product_id: productId, quantity }
      })
      if (res.success) {
        await fetchCart()
      }
      return res
    } catch (error) {
      console.error('Error updating cart item:', error)
      return { success: false, message: 'Failed to update cart item' }
    }
  }

  const removeItem = async (productId) => {
    if (!isAuthenticated()) {
      throw new Error('Please login to update cart')
    }

    try {
      const res = await apiCall('/api/cart/remove', {
        method: 'DELETE',
        body: { product_id: productId }
      })
      if (res.success) {
        await fetchCart()
      }
      return res
    } catch (error) {
      console.error('Error removing cart item:', error)
      return { success: false, message: 'Failed to remove cart item' }
    }
  }

  const clearCart = async () => {
    if (!isAuthenticated()) {
      throw new Error('Please login to clear cart')
    }

    try {
      const res = await apiCall('/api/cart/clear', { method: 'POST' })
      if (res.success) {
        await fetchCart()
      }
      return res
    } catch (error) {
      console.error('Error clearing cart:', error)
      return { success: false, message: 'Failed to clear cart' }
    }
  }

  const getCartCount = async () => {
    if (!isAuthenticated()) {
      cartCount.value = 0
      return 0
    }

    try {
      const res = await apiCall('/api/cart/count', { method: 'GET' })
      if (res.success) {
        cartCount.value = res.count
        return res.count
      }
    } catch (error) {
      console.error('Error getting cart count:', error)
    }
    return 0
  }

  const isInCart = (productId) => {
    return items.value.some(item => item.product && item.product.id === productId)
  }

  const getItemQuantity = (productId) => {
    const item = items.value.find(item => item.product && item.product.id === productId)
    return item ? item.quantity : 0
  }

  // Calculate total with tax/shipping if needed
  const calculateTotal = (shippingCost = 0, taxRate = 0) => {
    const subtotal = totals.value.subtotal || 0
    const tax = subtotal * taxRate
    const total = subtotal + shippingCost + tax
    return {
      subtotal,
      shipping: shippingCost,
      tax,
      total
    }
  }

  return { 
    items, 
    totals, 
    loading, 
    cartCount,
    fetchCart, 
    addItem, 
    updateItem, 
    removeItem, 
    clearCart,
    getCartCount,
    isInCart,
    getItemQuantity,
    calculateTotal
  }
}


