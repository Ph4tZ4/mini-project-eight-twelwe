// composables/useCart.js
export const useCart = () => {
  const { apiCall, isAuthenticated } = useApi()

  const items = useState('cart_items', () => [])
  const totals = useState('cart_totals', () => ({ subtotal: 0, total_quantity: 0 }))
  const loading = useState('cart_loading', () => false)

  const fetchCart = async () => {
    if (!isAuthenticated()) {
      items.value = []
      totals.value = { subtotal: 0, total_quantity: 0 }
      return
    }
    loading.value = true
    try {
      const res = await apiCall('/api/cart', { method: 'GET' })
      if (res.success) {
        items.value = res.cart.items
        totals.value = res.cart.totals
      }
    } finally {
      loading.value = false
    }
  }

  const addItem = async (productId, quantity = 1) => {
    const res = await apiCall('/api/cart/add', {
      method: 'POST',
      body: { product_id: productId, quantity }
    })
    if (res.success) {
      await fetchCart()
    }
    return res
  }

  const updateItem = async (productId, quantity) => {
    const res = await apiCall('/api/cart/update', {
      method: 'PUT',
      body: { product_id: productId, quantity }
    })
    if (res.success) {
      await fetchCart()
    }
    return res
  }

  const removeItem = async (productId) => {
    const res = await apiCall('/api/cart/remove', {
      method: 'DELETE',
      body: { product_id: productId }
    })
    if (res.success) {
      await fetchCart()
    }
    return res
  }

  const clearCart = async () => {
    const res = await apiCall('/api/cart/clear', { method: 'POST' })
    if (res.success) {
      await fetchCart()
    }
    return res
  }

  return { items, totals, loading, fetchCart, addItem, updateItem, removeItem, clearCart }
}


