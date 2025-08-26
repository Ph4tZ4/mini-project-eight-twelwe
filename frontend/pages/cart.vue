<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
        <div class="flex items-center gap-4">
          <NuxtLink to="/products" class="text-gray-300 hover:text-white transition-colors">
            กลับไปช้อปต่อ
          </NuxtLink>
          <div class="text-sm text-gray-400">
            {{ totals.total_quantity }} รายการ
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Title -->
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold">ตะกร้าสินค้า</h1>
        <button 
          v-if="items.length > 0" 
          @click="confirmClearCart"
          class="text-red-400 hover:text-red-300 text-sm transition-colors"
        >
          ล้างตะกร้า
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-400">กำลังโหลด...</p>
      </div>

      <!-- Main Cart Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Empty Cart -->
          <div v-if="items.length === 0" class="p-8 border border-gray-800 rounded-lg text-center">
            <div class="mb-4">
              <svg class="w-16 h-16 text-gray-600 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0H17"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-300 mb-2">ตะกร้าของคุณว่างเปล่า</h3>
            <p class="text-gray-500 mb-6">เริ่มเลือกซื้อสินค้าที่คุณชื่นชอบกันเถอะ</p>
            <NuxtLink 
              to="/products" 
              class="inline-block bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
            >
              เริ่มช้อปปิ้ง
            </NuxtLink>
          </div>

          <!-- Cart Items List -->
          <div v-for="item in items" :key="item.product.id" class="bg-gray-900 rounded-lg p-6 transition-all hover:bg-gray-850">
            <div class="flex gap-4">
              <!-- Product Image -->
              <div class="w-24 h-24 bg-gray-800 rounded-lg overflow-hidden flex-shrink-0">
                <img 
                  v-if="item.product.images && item.product.images[0]" 
                  :src="item.product.images[0]" 
                  :alt="item.product.name"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>

              <!-- Product Details -->
              <div class="flex-1 min-w-0">
                <div class="flex justify-between items-start mb-2">
                  <div class="flex-1">
                    <h3 class="font-semibold text-white truncate">{{ item.product.name }}</h3>
                    <p class="text-gray-400 text-sm">฿{{ formatPrice(item.price_at_add) }} ต่อชิ้น</p>
                    <p v-if="item.product.stock_quantity < 10" class="text-orange-400 text-xs mt-1">
                      เหลือเพียง {{ item.product.stock_quantity }} ชิ้น
                    </p>
                  </div>
                  <button 
                    @click="remove(item.product.id)"
                    class="text-gray-400 hover:text-red-400 p-1 transition-colors"
                    title="ลบสินค้า"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>

                <!-- Quantity Controls -->
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <button 
                      @click="decrease(item)"
                      :disabled="item.quantity <= 1"
                      class="w-8 h-8 rounded-full border border-gray-600 flex items-center justify-center hover:border-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
                      </svg>
                    </button>
                    
                    <input 
                      :value="item.quantity" 
                      @change="(e) => changeQty(item, e.target.value)"
                      class="w-16 text-center bg-gray-800 border border-gray-600 rounded-lg py-2 focus:border-white focus:outline-none transition-colors"
                      type="number"
                      min="1"
                      :max="item.product.stock_quantity"
                    />
                    
                    <button 
                      @click="increase(item)"
                      :disabled="item.quantity >= item.product.stock_quantity"
                      class="w-8 h-8 rounded-full border border-gray-600 flex items-center justify-center hover:border-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                      </svg>
                    </button>
                  </div>

                  <!-- Item Total -->
                  <div class="text-right">
                    <p class="font-semibold text-lg">฿{{ formatPrice(item.price_at_add * item.quantity) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="border border-gray-800 rounded-lg p-6 h-fit sticky top-24 bg-gray-900">
          <h2 class="text-xl font-semibold mb-6 border-b border-gray-800 pb-3">สรุปคำสั่งซื้อ</h2>
          
          <div class="space-y-3 mb-6">
            <div class="flex justify-between text-gray-300">
              <span>ยอดรวมสินค้า ({{ totals.total_quantity }} รายการ)</span>
              <span>฿{{ formatPrice(totals.subtotal) }}</span>
            </div>
            <div class="flex justify-between text-gray-300">
              <span>ค่าจัดส่ง</span>
              <span class="text-green-400">ฟรี</span>
            </div>
            <hr class="border-gray-700">
            <div class="flex justify-between text-white text-lg font-semibold">
              <span>ยอดรวมทั้งหมด</span>
              <span>฿{{ formatPrice(totals.subtotal) }}</span>
            </div>
          </div>

          <NuxtLink
            to="/checkout"
            :disabled="items.length === 0 || loading"
            class="block w-full bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors mb-3 text-center"
            :class="{ 'pointer-events-none opacity-50': items.length === 0 || loading }"
          >
            {{ loading ? 'กำลังดำเนินการ...' : 'ดำเนินการชำระเงิน' }}
          </NuxtLink>

          <NuxtLink 
            to="/products"
            class="block w-full text-center py-3 border border-gray-600 rounded-lg text-gray-300 hover:border-white hover:text-white transition-colors"
          >
            เลือกซื้อสินค้าเพิ่ม
          </NuxtLink>
        </div>
      </div>
    </main>

    <!-- Notification -->
    <div 
      v-if="notification.show" 
      class="fixed bottom-4 right-4 z-50 transition-all duration-300"
      :class="notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'"
    >
      <div class="px-6 py-4 rounded-lg text-white max-w-sm">
        <div class="flex items-center gap-2">
          <svg v-if="notification.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          <span>{{ notification.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'default' })

const { items, totals, loading, fetchCart, updateItem, removeItem, clearCart } = useCart()

// Notification system
const notification = ref({ show: false, message: '', type: 'success' })

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

// Utility functions
const formatPrice = (p) => Number(p || 0).toLocaleString('th-TH')

// Cart operations
const decrease = async (item) => {
  const q = Math.max(1, (item.quantity || 1) - 1)
  try {
    const result = await updateItem(item.product.id, q)
    if (result.success) {
      showNotification('อัปเดตจำนวนสินค้าแล้ว')
    } else {
      showNotification(result.message || 'เกิดข้อผิดพลาด', 'error')
    }
  } catch (error) {
    showNotification('เกิดข้อผิดพลาดในการอัปเดต', 'error')
  }
}

const increase = async (item) => {
  const q = (item.quantity || 1) + 1
  if (q > item.product.stock_quantity) {
    showNotification(`มีสินค้าเหลือเพียง ${item.product.stock_quantity} ชิ้น`, 'error')
    return
  }
  
  try {
    const result = await updateItem(item.product.id, q)
    if (result.success) {
      showNotification('อัปเดตจำนวนสินค้าแล้ว')
    } else {
      showNotification(result.message || 'เกิดข้อผิดพลาด', 'error')
    }
  } catch (error) {
    showNotification('เกิดข้อผิดพลาดในการอัปเดต', 'error')
  }
}

const changeQty = async (item, value) => {
  const q = Math.max(1, parseInt(value || '1', 10))
  if (q > item.product.stock_quantity) {
    showNotification(`มีสินค้าเหลือเพียง ${item.product.stock_quantity} ชิ้น`, 'error')
    return
  }
  
  try {
    const result = await updateItem(item.product.id, q)
    if (result.success) {
      showNotification('อัปเดตจำนวนสินค้าแล้ว')
    } else {
      showNotification(result.message || 'เกิดข้อผิดพลาด', 'error')
    }
  } catch (error) {
    showNotification('เกิดข้อผิดพลาดในการอัปเดต', 'error')
  }
}

const remove = async (productId) => {
  try {
    const result = await removeItem(productId)
    if (result.success) {
      showNotification('ลบสินค้าออกจากตะกร้าแล้ว')
    } else {
      showNotification(result.message || 'เกิดข้อผิดพลาด', 'error')
    }
  } catch (error) {
    showNotification('เกิดข้อผิดพลาดในการลบสินค้า', 'error')
  }
}

const confirmClearCart = () => {
  if (confirm('คุณต้องการลบสินค้าทั้งหมดในตะกร้าหรือไม่?')) {
    clearCartHandler()
  }
}

const clearCartHandler = async () => {
  try {
    const result = await clearCart()
    if (result.success) {
      showNotification('ล้างตะกร้าเรียบร้อยแล้ว')
    } else {
      showNotification(result.message || 'เกิดข้อผิดพลาด', 'error')
    }
  } catch (error) {
    showNotification('เกิดข้อผิดพลาดในการล้างตะกร้า', 'error')
  }
}



// Load cart on component mount
onMounted(() => {
  fetchCart()
})

// Provide cart to child components if needed
provide('cart', { items, totals, loading })
</script>


