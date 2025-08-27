<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button
            @click="goBack"
            class="text-gray-400 hover:text-white transition-colors p-2"
            title="ย้อนกลับ"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <h1 class="text-2xl font-bold text-white">โปรไฟล์ของฉัน</h1>
        </div>
        
        <div class="flex items-center gap-3">
          <NuxtLink
            to="/edit-profile"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors duration-200 text-sm"
          >
            แก้ไขโปรไฟล์
          </NuxtLink>
          <button
            @click="logout"
            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md transition-colors duration-200 text-sm"
          >
            ออกจากระบบ
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p class="text-gray-400">กำลังโหลดข้อมูล...</p>
        </div>
      </div>

      <!-- Profile Content -->
      <div v-else class="space-y-8">
        <!-- User Information Section -->
        <div class="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800">
            <h2 class="text-xl font-semibold text-white flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              ข้อมูลผู้ใช้
            </h2>
          </div>
          
          <div class="p-6">
            <div class="flex flex-col md:flex-row gap-6">
              <!-- Profile Picture -->
              <div class="flex-shrink-0">
                <div class="w-24 h-24 rounded-full overflow-hidden border-4 border-gray-700 mx-auto md:mx-0">
                  <img
                    v-if="user?.profile_picture"
                    :src="user.profile_picture"
                    :alt="user?.username"
                    class="w-full h-full object-cover"
                  />
                  <div
                    v-else
                    class="w-full h-full bg-gray-700 flex items-center justify-center text-2xl font-bold text-white"
                  >
                    {{ getUserInitials(user?.username) }}
                  </div>
                </div>
              </div>

              <!-- User Details -->
              <div class="flex-1 space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="text-sm text-gray-400">ชื่อผู้ใช้</label>
                    <p class="text-lg font-semibold text-white">{{ user?.username || '-' }}</p>
                  </div>
                  
                  <div>
                    <label class="text-sm text-gray-400">วันที่สมัครสมาชิก</label>
                    <p class="text-lg text-white">{{ formatDate(user?.created_at) }}</p>
                  </div>
                  
                  <div>
                    <label class="text-sm text-gray-400">ชื่อจริง</label>
                    <p class="text-lg text-white">{{ user?.first_name || '-' }}</p>
                  </div>
                  
                  <div>
                    <label class="text-sm text-gray-400">นามสกุล</label>
                    <p class="text-lg text-white">{{ user?.last_name || '-' }}</p>
                  </div>
                </div>

                <!-- Quick Stats -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-800">
                  <div class="text-center">
                    <p class="text-2xl font-bold text-blue-400">{{ totalOrders }}</p>
                    <p class="text-sm text-gray-400">คำสั่งซื้อทั้งหมด</p>
                  </div>
                  <div class="text-center">
                    <p class="text-2xl font-bold text-green-400">฿{{ formatPrice(totalSpent) }}</p>
                    <p class="text-sm text-gray-400">ยอดซื้อทั้งหมด</p>
                  </div>
                  <div class="text-center">
                    <p class="text-2xl font-bold text-yellow-400">{{ pendingOrders }}</p>
                    <p class="text-sm text-gray-400">รอจัดส่ง</p>
                  </div>
                  <div class="text-center">
                    <p class="text-2xl font-bold text-purple-400">{{ completedOrders }}</p>
                    <p class="text-sm text-gray-400">สำเร็จแล้ว</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order History Section -->
        <div class="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <h2 class="text-xl font-semibold text-white flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                ประวัติการสั่งซื้อ
              </h2>
              
              <!-- Filter & Search -->
              <div class="flex flex-col sm:flex-row gap-2">
                <select 
                  v-model="statusFilter"
                  @change="applyFilters"
                  class="bg-gray-800 border border-gray-700 text-white px-3 py-2 rounded-md text-sm"
                >
                  <option value="">ทุกสถานะ</option>
                  <option value="pending">รอดำเนินการ</option>
                  <option value="confirmed">ยืนยันแล้ว</option>
                  <option value="processing">กำลังเตรียมสินค้า</option>
                  <option value="shipped">จัดส่งแล้ว</option>
                  <option value="delivered">จัดส่งสำเร็จ</option>
                  <option value="cancelled">ยกเลิก</option>
                </select>
                
                <NuxtLink 
                  to="/orders"
                  class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors text-sm text-center"
                >
                  ดูทั้งหมด
                </NuxtLink>
              </div>
            </div>
          </div>

          <div class="p-6">
            <!-- Loading Orders -->
            <div v-if="ordersLoading" class="text-center py-8">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
              <p class="mt-2 text-gray-400">กำลังโหลดคำสั่งซื้อ...</p>
            </div>

            <!-- No Orders -->
            <div v-else-if="filteredOrders.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
              <h3 class="text-lg font-semibold text-gray-300 mb-2">
                {{ statusFilter ? 'ไม่พบคำสั่งซื้อในสถานะนี้' : 'ยังไม่มีคำสั่งซื้อ' }}
              </h3>
              <p class="text-gray-500 mb-4">เริ่มเลือกซื้อสินค้าที่คุณชื่นชอบกันเถอะ</p>
              <NuxtLink 
                to="/products" 
                class="inline-block bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
              >
                เลือกซื้อสินค้า
              </NuxtLink>
            </div>

            <!-- Orders List -->
            <div v-else class="space-y-4">
              <div 
                v-for="order in displayedOrders" 
                :key="order.id"
                class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden hover:border-gray-600 transition-colors"
              >
                <!-- Order Header -->
                <div class="p-4 border-b border-gray-700">
                  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                      <h3 class="font-semibold text-white text-sm">
                        คำสั่งซื้อ #{{ order.order_number }}
                      </h3>
                      <p class="text-xs text-gray-400">
                        {{ formatDate(order.created_at) }}
                      </p>
                    </div>
                    
                    <div class="flex items-center gap-2">
                      <span class="px-2 py-1 rounded-full text-xs font-semibold"
                            :class="getOrderStatusClass(order.order_status)">
                        {{ getOrderStatusText(order.order_status) }}
                      </span>
                      <span class="text-sm font-semibold text-white">
                        ฿{{ formatPrice(order.total_amount) }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Order Items Preview -->
                <div class="p-4">
                  <div class="space-y-2 mb-3">
                    <div 
                      v-for="item in order.items.slice(0, 2)" 
                      :key="item.product_name"
                      class="flex items-center gap-3 text-sm"
                    >
                      <div class="w-8 h-8 bg-gray-700 rounded flex items-center justify-center flex-shrink-0">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                        </svg>
                      </div>
                      <div class="flex-1">
                        <p class="text-white">{{ item.product_name }}</p>
                        <p class="text-gray-400">จำนวน {{ item.quantity }} x ฿{{ formatPrice(item.price_at_order) }}</p>
                      </div>
                    </div>
                    
                    <p v-if="order.items.length > 2" class="text-xs text-gray-400 ml-11">
                      และอีก {{ order.items.length - 2 }} รายการ
                    </p>
                  </div>

                  <!-- Action Buttons -->
                  <div class="flex flex-col sm:flex-row gap-2">
                    <button 
                      @click="viewOrderDetails(order)"
                      class="flex-1 bg-gray-700 text-white py-2 px-3 rounded text-sm hover:bg-gray-600 transition-colors"
                    >
                      ดูรายละเอียด
                    </button>
                    
                    <NuxtLink 
                      v-if="order.tracking_number"
                      :to="`/tracking/${order.tracking_number}`"
                      class="flex-1 bg-blue-600 text-white py-2 px-3 rounded text-sm hover:bg-blue-700 transition-colors text-center"
                    >
                      ติดตามสินค้า
                    </NuxtLink>
                    
                    <button 
                      v-if="canReorder(order)"
                      @click="reorder(order)"
                      :disabled="reordering"
                      class="flex-1 bg-white text-black py-2 px-3 rounded text-sm hover:bg-gray-200 disabled:opacity-50 transition-colors"
                    >
                      {{ reordering ? 'กำลังเพิ่ม...' : 'สั่งซื้อซ้ำ' }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Show More Button -->
              <div v-if="filteredOrders.length > displayLimit" class="text-center pt-4">
                <button 
                  @click="showMore"
                  class="bg-gray-700 text-white py-2 px-6 rounded-lg hover:bg-gray-600 transition-colors text-sm"
                >
                  แสดงเพิ่มเติม ({{ filteredOrders.length - displayLimit }} รายการ)
                </button>
              </div>
            </div>
          </div>
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

const { apiCall, isAuthenticated, getCurrentUser, logout: apiLogout } = useApi()
const { addItem } = useCart()

// State
const loading = ref(true)
const ordersLoading = ref(true)
const reordering = ref(false)
const user = ref(null)
const orders = ref([])
const filteredOrders = ref([])
const selectedOrder = ref(null)
const statusFilter = ref('')
const displayLimit = ref(5)

// Computed stats
const totalOrders = computed(() => orders.value.length)
const totalSpent = computed(() => orders.value.reduce((sum, order) => sum + (order.total_amount || 0), 0))
const pendingOrders = computed(() => orders.value.filter(order => 
  ['pending', 'confirmed', 'processing', 'shipped'].includes(order.order_status)
).length)
const completedOrders = computed(() => orders.value.filter(order => 
  order.order_status === 'delivered'
).length)

const displayedOrders = computed(() => filteredOrders.value.slice(0, displayLimit.value))

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
  if (!dateString) return 'ไม่ทราบ'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('th-TH', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return 'ไม่ทราบ'
  }
}

const getUserInitials = (username) => {
  if (!username) return 'U'
  
  const words = username.match(/[A-Z][a-z]*|[a-z]+/g)
  
  if (!words) {
    return username[0]?.toUpperCase() || 'U'
  }
  
  const initials = words.slice(0, 2).map(word => word[0].toUpperCase()).join('')
  return initials || username[0]?.toUpperCase() || 'U'
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

// Load user profile
const loadUserProfile = async () => {
  try {
    const response = await apiCall('/api/profile')
    user.value = response.user
  } catch (error) {
    console.error('Error loading profile:', error)
    showNotification('ไม่สามารถโหลดข้อมูลผู้ใช้ได้', 'error')
  }
}

// Load orders
const loadOrders = async () => {
  try {
    ordersLoading.value = true
    const response = await apiCall('/api/orders')
    
    if (response.success) {
      orders.value = response.orders
      applyFilters()
    } else {
      showNotification('ไม่สามารถโหลดคำสั่งซื้อได้', 'error')
    }
  } catch (error) {
    console.error('Error fetching orders:', error)
    showNotification('เกิดข้อผิดพลาดในการโหลดข้อมูล', 'error')
  } finally {
    ordersLoading.value = false
  }
}

const applyFilters = () => {
  if (!statusFilter.value) {
    filteredOrders.value = orders.value
  } else {
    filteredOrders.value = orders.value.filter(order => order.order_status === statusFilter.value)
  }
  displayLimit.value = 5 // Reset display limit when filtering
}

const showMore = () => {
  displayLimit.value += 5
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

const goBack = () => {
  navigateTo('/home')
}

const logout = () => {
  apiLogout()
}

// Lifecycle
onMounted(async () => {
  if (!isAuthenticated()) {
    await navigateTo('/login')
    return
  }

  try {
    loading.value = true
    await Promise.all([
      loadUserProfile(),
      loadOrders()
    ])
  } catch (error) {
    console.error('Error loading profile data:', error)
  } finally {
    loading.value = false
  }
})

// Head
useHead({
  title: 'โปรไฟล์ของฉัน - ShopHub'
})
</script>

<style scoped>
/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #1f1f1f;
}

::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6a6a6a;
}
</style>