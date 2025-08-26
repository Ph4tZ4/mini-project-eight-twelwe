<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
        <div class="flex items-center gap-4">
          <NuxtLink to="/orders" class="text-gray-300 hover:text-white transition-colors">
            คำสั่งซื้อของฉัน
          </NuxtLink>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-400">กำลังโหลดข้อมูลคำสั่งซื้อ...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h2 class="text-2xl font-bold text-red-400 mb-4">ไม่พบคำสั่งซื้อ</h2>
        <p class="text-gray-400 mb-6">{{ error }}</p>
        <NuxtLink 
          to="/products" 
          class="inline-block bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
        >
          เลือกซื้อสินค้า
        </NuxtLink>
      </div>

      <!-- Success State -->
      <div v-else class="space-y-8">
        <!-- Success Header -->
        <div class="text-center bg-green-900 border border-green-700 rounded-lg p-8">
          <div class="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-green-400 mb-2">สั่งซื้อสำเร็จ!</h1>
          <p class="text-gray-300 mb-4">ขอบคุณสำหรับการสั่งซื้อ คำสั่งซื้อของคุณได้รับการยืนยันแล้ว</p>
          <div class="bg-black rounded-lg p-4 inline-block">
            <p class="text-sm text-gray-400">หมายเลขคำสั่งซื้อ</p>
            <p class="text-2xl font-bold text-white">{{ order.order_number }}</p>
          </div>
        </div>

        <!-- Order Details -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Order Information -->
          <div class="bg-gray-900 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 border-b border-gray-800 pb-3">ข้อมูลคำสั่งซื้อ</h2>
            
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-400">หมายเลขคำสั่งซื้อ:</span>
                <span class="font-semibold">{{ order.order_number }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-400">สถานะ:</span>
                <span class="px-2 py-1 rounded text-xs font-semibold"
                      :class="getOrderStatusClass(order.order_status)">
                  {{ getOrderStatusText(order.order_status) }}
                </span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-400">วันที่สั่งซื้อ:</span>
                <span>{{ formatDate(order.created_at) }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-400">วิธีการชำระเงิน:</span>
                <span>{{ getPaymentMethodText(order.payment.method) }}</span>
              </div>
              
              <div v-if="order.tracking" class="flex justify-between">
                <span class="text-gray-400">หมายเลขติดตาม:</span>
                <NuxtLink 
                  :to="`/tracking/${order.tracking.tracking_number}`"
                  class="text-blue-400 hover:text-blue-300 underline"
                >
                  {{ order.tracking.tracking_number }}
                </NuxtLink>
              </div>
            </div>
          </div>

          <!-- Shipping Address -->
          <div class="bg-gray-900 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 border-b border-gray-800 pb-3">ที่อยู่สำหรับจัดส่ง</h2>
            
            <div class="space-y-2">
              <p class="font-semibold">{{ order.shipping_address.full_name }}</p>
              <p class="text-gray-300">{{ order.shipping_address.phone }}</p>
              <p class="text-gray-300">{{ order.shipping_address.address_line_1 }}</p>
              <p v-if="order.shipping_address.address_line_2" class="text-gray-300">
                {{ order.shipping_address.address_line_2 }}
              </p>
              <p class="text-gray-300">
                {{ order.shipping_address.city }}, {{ order.shipping_address.province }} 
                {{ order.shipping_address.postal_code }}
              </p>
              <p class="text-gray-300">{{ order.shipping_address.country }}</p>
            </div>
          </div>
        </div>

        <!-- Order Items -->
        <div class="bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-4 border-b border-gray-800 pb-3">รายการสินค้า</h2>
          
          <div class="space-y-4">
            <div v-for="item in order.items" :key="item.product.id" 
                 class="flex gap-4 p-4 border border-gray-800 rounded-lg">
              <!-- Product Image -->
              <div class="w-16 h-16 bg-gray-800 rounded-lg overflow-hidden flex-shrink-0">
                <img 
                  v-if="item.product.images && item.product.images[0]" 
                  :src="item.product.images[0]" 
                  :alt="item.product.name"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              
              <!-- Product Details -->
              <div class="flex-1">
                <h3 class="font-semibold text-white">{{ item.product.name }}</h3>
                <p class="text-sm text-gray-400">จำนวน: {{ item.quantity }}</p>
                <p class="text-sm text-gray-400">ราคา: ฿{{ formatPrice(item.price_at_order) }}</p>
              </div>
              
              <!-- Item Total -->
              <div class="text-right">
                <p class="font-semibold text-lg">฿{{ formatPrice(item.total_price) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-4 border-b border-gray-800 pb-3">สรุปยอดเงิน</h2>
          
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-400">ยอดรวมสินค้า:</span>
              <span>฿{{ formatPrice(order.subtotal) }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-gray-400">ค่าจัดส่ง:</span>
              <span>{{ order.shipping_fee > 0 ? `฿${formatPrice(order.shipping_fee)}` : 'ฟรี' }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-gray-400">ภาษี:</span>
              <span>฿{{ formatPrice(order.tax) }}</span>
            </div>
            
            <hr class="border-gray-700">
            
            <div class="flex justify-between text-xl font-semibold">
              <span>ยอดรวมทั้งหมด:</span>
              <span>฿{{ formatPrice(order.total_amount) }}</span>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-4">
          <NuxtLink 
            v-if="order.tracking"
            :to="`/tracking/${order.tracking.tracking_number}`"
            class="flex-1 bg-blue-600 text-white text-center py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            ติดตามสินค้า
          </NuxtLink>
          
          <NuxtLink 
            to="/orders"
            class="flex-1 bg-gray-700 text-white text-center py-3 px-6 rounded-lg font-semibold hover:bg-gray-600 transition-colors"
          >
            ดูคำสั่งซื้อทั้งหมด
          </NuxtLink>
          
          <NuxtLink 
            to="/products"
            class="flex-1 bg-white text-black text-center py-3 px-6 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
          >
            เลือกซื้อสินค้าเพิ่ม
          </NuxtLink>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({ 
  layout: 'default',
  middleware: 'auth',
  ssr: false
})

const route = useRoute()
const { apiCall } = useApi()

// State
const loading = ref(true)
const error = ref(null)
const order = ref(null)

// Get order number from route
const orderNumber = computed(() => route.params.orderNumber)

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

const getPaymentMethodText = (method) => {
  const methodTexts = {
    'cash_on_delivery': 'เก็บเงินปลายทาง',
    'credit_card': 'บัตรเครดิต',
    'bank_transfer': 'โอนเงินผ่านธนาคาร'
  }
  return methodTexts[method] || method
}

const fetchOrderDetails = async () => {
  try {
    loading.value = true
    
    // First try to get from orders list
    const ordersResponse = await apiCall('/api/orders')
    if (ordersResponse.success) {
      const foundOrder = ordersResponse.orders.find(o => o.order_number === orderNumber.value)
      if (foundOrder) {
        // Get detailed order info
        const detailResponse = await apiCall(`/api/orders/${foundOrder.id}`)
        if (detailResponse.success) {
          order.value = detailResponse.order
        } else {
          error.value = 'ไม่สามารถโหลดรายละเอียดคำสั่งซื้อได้'
        }
      } else {
        error.value = 'ไม่พบคำสั่งซื้อนี้'
      }
    } else {
      error.value = 'ไม่สามารถโหลดข้อมูลคำสั่งซื้อได้'
    }
  } catch (err) {
    console.error('Error fetching order:', err)
    error.value = 'เกิดข้อผิดพลาดในการโหลดข้อมูล'
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchOrderDetails()
})

// Head
useHead({
  title: computed(() => 
    order.value ? `ยืนยันคำสั่งซื้อ ${order.value.order_number} - ShopHub` : 'ยืนยันคำสั่งซื้อ - ShopHub'
  )
})
</script>
