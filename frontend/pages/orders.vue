<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
        <div class="flex items-center gap-4">
          <!-- Cart Icon -->
          <NuxtLink
            to="/cart"
            class="relative text-gray-300 hover:text-white transition-colors p-2"
            title="ตะกร้าสินค้า"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0H17"></path>
            </svg>
            <span 
              v-if="cartCount > 0" 
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartCount > 99 ? '99+' : cartCount }}
            </span>
          </NuxtLink>
          
          <NuxtLink to="/products" class="text-gray-300 hover:text-white transition-colors">
            เลือกซื้อสินค้า
          </NuxtLink>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">คำสั่งซื้อของฉัน</h1>
        <p class="text-gray-400">ดูประวัติการสั่งซื้อและติดตามสถานะสินค้า</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-400">กำลังโหลดคำสั่งซื้อ...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="orders.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        <h2 class="text-xl font-semibold text-gray-300 mb-2">ยังไม่มีคำสั่งซื้อ</h2>
        <p class="text-gray-500 mb-6">เริ่มเลือกซื้อสินค้าที่คุณชื่นชอบกันเถอะ</p>
        <NuxtLink 
          to="/products" 
          class="inline-block bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
        >
          เลือกซื้อสินค้า
        </NuxtLink>
      </div>

      <!-- Orders List -->
      <div v-else class="space-y-6">
        <div v-for="order in orders" :key="order.id" 
             class="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
          
          <!-- Order Header -->
          <div class="p-6 border-b border-gray-800">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h3 class="text-lg font-semibold text-white mb-1">
                  คำสั่งซื้อ #{{ order.order_number }}
                </h3>
                <p class="text-sm text-gray-400">
                  สั่งซื้อเมื่อ {{ formatDate(order.created_at) }}
                </p>
              </div>
              
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-full text-xs font-semibold"
                      :class="getOrderStatusClass(order.order_status)">
                  {{ getOrderStatusText(order.order_status) }}
                </span>
                
                <span class="px-3 py-1 rounded-full text-xs font-semibold"
                      :class="getPaymentStatusClass(order.payment_status)">
                  {{ getPaymentStatusText(order.payment_status) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div class="p-6">
            <div class="space-y-3 mb-4">
              <div v-for="item in order.items" :key="`${order.id}-${item.product_name}`"
                   class="flex items-center gap-4">
                <div class="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg>
                </div>
                
                <div class="flex-1">
                  <h4 class="font-medium text-white">{{ item.product_name }}</h4>
                  <p class="text-sm text-gray-400">
                    จำนวน {{ item.quantity }} x ฿{{ formatPrice(item.price_at_order) }}
                  </p>
                </div>
                
                <div class="text-right">
                  <p class="font-semibold text-white">฿{{ formatPrice(item.total_price) }}</p>
                </div>
              </div>
            </div>

            <!-- Order Summary -->
            <div class="border-t border-gray-800 pt-4">
              <div class="flex justify-between items-center mb-4">
                <div>
                  <p class="text-sm text-gray-400">วิธีการชำระเงิน</p>
                  <p class="font-medium">{{ getPaymentMethodText(order.payment_method) }}</p>
                </div>
                
                <div class="text-right">
                  <p class="text-sm text-gray-400">ยอดรวมทั้งหมด</p>
                  <p class="text-xl font-bold text-white">฿{{ formatPrice(order.total_amount) }}</p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex flex-col sm:flex-row gap-3">
                <button 
                  @click="viewOrderDetails(order)"
                  class="flex-1 bg-gray-700 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition-colors"
                >
                  ดูรายละเอียด
                </button>
                
                <NuxtLink 
                  v-if="order.tracking_number"
                  :to="`/tracking/${order.tracking_number}`"
                  class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-center"
                >
                  ติดตามสินค้า
                </NuxtLink>
                
                <button 
                  v-if="canReorder(order)"
                  @click="reorder(order)"
                  :disabled="reordering"
                  class="flex-1 bg-white text-black py-2 px-4 rounded-lg hover:bg-gray-200 disabled:opacity-50 transition-colors"
                >
                  {{ reordering ? 'กำลังเพิ่ม...' : 'สั่งซื้อซ้ำ' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMore" class="text-center">
          <button 
            @click="loadMore"
            :disabled="loadingMore"
            class="bg-gray-700 text-white py-3 px-6 rounded-lg hover:bg-gray-600 disabled:opacity-50 transition-colors"
          >
            {{ loadingMore ? 'กำลังโหลด...' : 'โหลดเพิ่มเติม' }}
          </button>
        </div>
      </div>
    </main>

    <!-- Order Details Modal -->
    <div v-if="selectedOrder" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
         @click="closeModal">
      <div class="bg-gray-900 rounded-lg max-w-2xl w-full max-h-screen overflow-y-auto"
           @click.stop>
        <div class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-white">
              รายละเอียดคำสั่งซื้อ #{{ selectedOrder.order_number }}
            </h2>
            <button @click="closeModal" class="text-gray-400 hover:text-white">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- Order Info -->
          <div class="space-y-4 mb-6">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-400">สถานะคำสั่งซื้อ</p>
                <span class="px-2 py-1 rounded text-xs font-semibold"
                      :class="getOrderStatusClass(selectedOrder.order_status)">
                  {{ getOrderStatusText(selectedOrder.order_status) }}
                </span>
              </div>
              
              <div>
                <p class="text-sm text-gray-400">สถานะการชำระเงิน</p>
                <span class="px-2 py-1 rounded text-xs font-semibold"
                      :class="getPaymentStatusClass(selectedOrder.payment_status)">
                  {{ getPaymentStatusText(selectedOrder.payment_status) }}
                </span>
              </div>
              
              <div>
                <p class="text-sm text-gray-400">วันที่สั่งซื้อ</p>
                <p class="font-medium">{{ formatDate(selectedOrder.created_at) }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-400">วิธีการชำระเงิน</p>
                <p class="font-medium">{{ getPaymentMethodText(selectedOrder.payment_method) }}</p>
              </div>
            </div>
          </div>

          <!-- Items -->
          <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">รายการสินค้า</h3>
            <div class="space-y-2">
              <div v-for="item in selectedOrder.items" :key="item.product_name"
                   class="flex justify-between items-center p-3 bg-gray-800 rounded">
                <div>
                  <p class="font-medium">{{ item.product_name }}</p>
                  <p class="text-sm text-gray-400">{{ item.quantity }} x ฿{{ formatPrice(item.price_at_order) }}</p>
                </div>
                <p class="font-semibold">฿{{ formatPrice(item.total_price) }}</p>
              </div>
            </div>
          </div>

          <!-- Total -->
          <div class="border-t border-gray-800 pt-4">
            <div class="flex justify-between items-center text-lg font-bold">
              <span>ยอดรวมทั้งหมด</span>
              <span>฿{{ formatPrice(selectedOrder.total_amount) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

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
definePageMeta({ 
  layout: 'default',
  middleware: 'auth'
})

const { apiCall } = useApi()
const { addItem, cartCount, getCartCount } = useCart()

// State
const loading = ref(true)
const loadingMore = ref(false)
const reordering = ref(false)
const orders = ref([])
const selectedOrder = ref(null)
const hasMore = ref(false)
const currentPage = ref(1)

// Notification system
const notification = ref({ show: false, message: '', type: 'success' })

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

// Methods
const formatPrice = (price) => Number(price || 0).toLocaleString('th-TH')

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getOrderStatusClass = (status) => {
  const statusClasses = {
    'pending': 'bg-yellow-600 text-yellow-100',
    'confirmed': 'bg-blue-600 text-blue-100',
    'processing': 'bg-purple-600 text-purple-100',
    'shipped': 'bg-indigo-600 text-indigo-100',
    'delivered': 'bg-green-600 text-green-100',
    'cancelled': 'bg-red-600 text-red-100'
  }
  return statusClasses[status] || 'bg-gray-600 text-gray-100'
}

const getOrderStatusText = (status) => {
  const statusTexts = {
    'pending': 'รอดำเนินการ',
    'confirmed': 'ยืนยันแล้ว',
    'processing': 'กำลังเตรียมสินค้า',
    'shipped': 'จัดส่งแล้ว',
    'delivered': 'จัดส่งสำเร็จ',
    'cancelled': 'ยกเลิก'
  }
  return statusTexts[status] || status
}

const getPaymentStatusClass = (status) => {
  const statusClasses = {
    'pending': 'bg-yellow-600 text-yellow-100',
    'paid': 'bg-green-600 text-green-100',
    'failed': 'bg-red-600 text-red-100',
    'refunded': 'bg-gray-600 text-gray-100'
  }
  return statusClasses[status] || 'bg-gray-600 text-gray-100'
}

const getPaymentStatusText = (status) => {
  const statusTexts = {
    'pending': 'รอชำระเงิน',
    'paid': 'ชำระเงินแล้ว',
    'failed': 'ชำระเงินไม่สำเร็จ',
    'refunded': 'คืนเงินแล้ว'
  }
  return statusTexts[status] || status
}

const getPaymentMethodText = (method) => {
  const methodTexts = {
    'cash_on_delivery': 'เก็บเงินปลายทาง',
    'credit_card': 'บัตรเครดิต',
    'bank_transfer': 'โอนเงินผ่านธนาคาร'
  }
  return methodTexts[method] || method
}

const canReorder = (order) => {
  return order.order_status === 'delivered'
}

const fetchOrders = async () => {
  try {
    loading.value = true
    const response = await apiCall('/api/orders')
    
    if (response.success) {
      orders.value = response.orders
    } else {
      showNotification('ไม่สามารถโหลดคำสั่งซื้อได้', 'error')
    }
  } catch (error) {
    console.error('Error fetching orders:', error)
    showNotification('เกิดข้อผิดพลาดในการโหลดข้อมูล', 'error')
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  // Implementation for pagination if needed
  loadingMore.value = true
  // Add pagination logic here
  loadingMore.value = false
}

const viewOrderDetails = (order) => {
  selectedOrder.value = order
}

const closeModal = () => {
  selectedOrder.value = null
}

const reorder = async (order) => {
  try {
    reordering.value = true
    
    // Add each item from the order to cart
    for (const item of order.items) {
      try {
        await addItem(item.product_id, item.quantity)
      } catch (error) {
        console.warn(`Could not add ${item.product_name} to cart:`, error)
      }
    }
    
    showNotification('เพิ่มสินค้าลงตะกร้าเรียบร้อยแล้ว', 'success')
    
    // Navigate to cart after a short delay
    setTimeout(() => {
      navigateTo('/cart')
    }, 1500)
    
  } catch (error) {
    console.error('Error reordering:', error)
    showNotification('เกิดข้อผิดพลาดในการสั่งซื้อซ้ำ', 'error')
  } finally {
    reordering.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    fetchOrders(),
    getCartCount()
  ])
})

// Head
useHead({
  title: 'คำสั่งซื้อของฉัน - ShopHub'
})
</script>
