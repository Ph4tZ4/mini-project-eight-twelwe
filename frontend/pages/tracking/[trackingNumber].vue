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

    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white mb-4">ติดตามการจัดส่ง</h1>
        <p class="text-gray-400">ตรวจสอบสถานะการจัดส่งสินค้าของคุณ</p>
      </div>

      <!-- Tracking Number Search -->
      <div class="bg-gray-900 rounded-lg p-6 mb-8">
        <div class="max-w-md mx-auto">
          <label class="block text-sm font-medium text-gray-300 mb-2">
            ค้นหาด้วยหมายเลขติดตาม
          </label>
          <div class="flex gap-2">
            <input
              v-model="searchTrackingNumber"
              type="text"
              placeholder="กรอกหมายเลขติดตาม"
              class="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
              @keyup.enter="searchTracking"
            />
            <button 
              @click="searchTracking"
              :disabled="!searchTrackingNumber || searching"
              class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {{ searching ? 'ค้นหา...' : 'ค้นหา' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-400">กำลังโหลดข้อมูลการจัดส่ง...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h2 class="text-2xl font-bold text-red-400 mb-4">ไม่พบข้อมูลการจัดส่ง</h2>
        <p class="text-gray-400 mb-6">{{ error }}</p>
        <button 
          @click="() => { error = null; searchTrackingNumber = ''; }"
          class="bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
        >
          ลองใหม่
        </button>
      </div>

      <!-- Tracking Information -->
      <div v-else-if="tracking" class="space-y-8">
        <!-- Tracking Header -->
        <div class="bg-gray-900 rounded-lg p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <h3 class="text-sm font-medium text-gray-400 mb-1">หมายเลขติดตาม</h3>
              <p class="text-lg font-semibold text-white">{{ tracking.tracking_number }}</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-400 mb-1">หมายเลขคำสั่งซื้อ</h3>
              <p class="text-lg font-semibold text-white">{{ tracking.order_info.order_number }}</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-400 mb-1">ผู้ให้บริการ</h3>
              <p class="text-lg font-semibold text-white">{{ tracking.carrier }}</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-400 mb-1">สถานะปัจจุบัน</h3>
              <span class="px-3 py-1 rounded-full text-sm font-semibold"
                    :class="getStatusClass(tracking.current_status)">
                {{ tracking.current_status_description }}
              </span>
            </div>
          </div>
        </div>

        <!-- Delivery Information -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Shipping Address -->
          <div class="bg-gray-900 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
              </svg>
              ที่อยู่จัดส่ง
            </h2>
            
            <div class="space-y-1 text-gray-300">
              <p class="font-semibold text-white">{{ tracking.shipping_address.full_name }}</p>
              <p>{{ tracking.shipping_address.city }}, {{ tracking.shipping_address.province }}</p>
              <p>{{ tracking.shipping_address.postal_code }}</p>
            </div>
          </div>

          <!-- Delivery Timeline -->
          <div class="bg-gray-900 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              กำหนดการจัดส่ง
            </h2>
            
            <div class="space-y-3">
              <div v-if="tracking.order_info.created_at">
                <p class="text-sm text-gray-400">วันที่สั่งซื้อ</p>
                <p class="font-semibold">{{ formatDate(tracking.order_info.created_at) }}</p>
              </div>
              
              <div v-if="tracking.estimated_delivery">
                <p class="text-sm text-gray-400">คาดการณ์วันจัดส่ง</p>
                <p class="font-semibold text-blue-400">{{ formatDate(tracking.estimated_delivery) }}</p>
              </div>
              
              <div v-if="tracking.actual_delivery">
                <p class="text-sm text-gray-400">จัดส่งเรียบร้อยแล้ว</p>
                <p class="font-semibold text-green-400">{{ formatDate(tracking.actual_delivery) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tracking Progress -->
        <div class="bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-6">สถานะการจัดส่ง</h2>
          
          <div class="relative">
            <div class="space-y-6">
              <div v-for="(status, index) in getTrackingSteps()" :key="status.key" 
                   class="flex items-center relative">
                <!-- Progress Line -->
                <div v-if="index < getTrackingSteps().length - 1" 
                     class="absolute left-6 top-12 w-0.5 h-6 bg-gray-700"
                     :class="{ 'bg-green-500': status.completed }">
                </div>
                
                <!-- Status Icon -->
                <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0"
                     :class="status.completed ? 'bg-green-600' : 'bg-gray-700'">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="status.completed" 
                          stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M5 13l4 4L19 7">
                    </path>
                    <circle v-else cx="12" cy="12" r="3"></circle>
                  </svg>
                </div>
                
                <!-- Status Content -->
                <div class="ml-4 flex-1">
                  <h3 class="font-semibold" :class="status.completed ? 'text-white' : 'text-gray-400'">
                    {{ status.title }}
                  </h3>
                  <p class="text-sm text-gray-400">{{ status.description }}</p>
                  <p v-if="status.timestamp" class="text-xs text-gray-500 mt-1">
                    {{ formatDate(status.timestamp) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed History -->
        <div v-if="tracking.status_history && tracking.status_history.length > 0" 
             class="bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-6">ประวัติการติดตาม</h2>
          
          <div class="space-y-4">
            <div v-for="history in tracking.status_history" :key="history.timestamp"
                 class="flex gap-4 p-4 border border-gray-800 rounded-lg">
              <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
              <div class="flex-1">
                <div class="flex justify-between items-start mb-1">
                  <h3 class="font-semibold text-white">{{ history.description }}</h3>
                  <span class="text-sm text-gray-400">{{ formatDate(history.timestamp) }}</span>
                </div>
                <p v-if="history.location" class="text-sm text-gray-400">
                  📍 {{ history.location }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-4">สรุปคำสั่งซื้อ</h2>
          
          <div class="flex justify-between items-center">
            <div>
              <p class="text-sm text-gray-400">หมายเลขคำสั่งซื้อ</p>
              <p class="font-semibold">{{ tracking.order_info.order_number }}</p>
            </div>
            
            <div class="text-right">
              <p class="text-sm text-gray-400">ยอดรวม</p>
              <p class="text-xl font-bold">฿{{ formatPrice(tracking.order_info.total_amount) }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'default' })

const route = useRoute()
const { apiCall } = useApi()

// State
const loading = ref(false)
const searching = ref(false)
const error = ref(null)
const tracking = ref(null)
const searchTrackingNumber = ref('')

// Get tracking number from route
const trackingNumber = computed(() => route.params.trackingNumber)

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

const getStatusClass = (status) => {
  const statusClasses = {
    'order_placed': 'bg-blue-600 text-blue-100',
    'preparing': 'bg-yellow-600 text-yellow-100',
    'picked_up': 'bg-purple-600 text-purple-100',
    'in_transit': 'bg-indigo-600 text-indigo-100',
    'out_for_delivery': 'bg-orange-600 text-orange-100',
    'delivered': 'bg-green-600 text-green-100'
  }
  return statusClasses[status] || 'bg-gray-600 text-gray-100'
}

const getTrackingSteps = () => {
  const steps = [
    {
      key: 'order_placed',
      title: 'คำสั่งซื้อได้รับการยืนยัน',
      description: 'เราได้รับคำสั่งซื้อของคุณแล้ว',
      completed: false,
      timestamp: null
    },
    {
      key: 'preparing',
      title: 'กำลังเตรียมสินค้า',
      description: 'เราดำลังเตรียมและตรวจสอบสินค้าของคุณ',
      completed: false,
      timestamp: null
    },
    {
      key: 'picked_up',
      title: 'สินค้าถูกรับเข้าระบบขนส่ง',
      description: 'สินค้าถูกส่งมอบให้ผู้ให้บริการขนส่งแล้ว',
      completed: false,
      timestamp: null
    },
    {
      key: 'in_transit',
      title: 'สินค้าอยู่ระหว่างการขนส่ง',
      description: 'สินค้าอยู่ระหว่างเดินทางไปยังปลายทาง',
      completed: false,
      timestamp: null
    },
    {
      key: 'out_for_delivery',
      title: 'สินค้าออกจัดส่ง',
      description: 'สินค้าออกจัดส่งและจะถึงคุณในไม่ช้า',
      completed: false,
      timestamp: null
    },
    {
      key: 'delivered',
      title: 'จัดส่งสำเร็จ',
      description: 'สินค้าถูกส่งมอบเรียบร้อยแล้ว',
      completed: false,
      timestamp: null
    }
  ]

  if (tracking.value) {
    // Mark completed steps based on current status
    const currentStatusIndex = steps.findIndex(step => step.key === tracking.value.current_status)
    
    for (let i = 0; i <= currentStatusIndex; i++) {
      steps[i].completed = true
    }

    // Add timestamps from history
    if (tracking.value.status_history) {
      tracking.value.status_history.forEach(history => {
        const step = steps.find(s => s.key === history.status)
        if (step) {
          step.timestamp = history.timestamp
        }
      })
    }
  }

  return steps
}

const fetchTracking = async (number = null) => {
  const trackingNum = number || trackingNumber.value
  if (!trackingNum) return

  try {
    loading.value = true
    error.value = null

    const response = await apiCall(`/api/tracking/${trackingNum}`)
    
    if (response.success) {
      tracking.value = response.tracking
    } else {
      error.value = response.message || 'ไม่พบข้อมูลการจัดส่ง'
    }
  } catch (err) {
    console.error('Error fetching tracking:', err)
    error.value = 'เกิดข้อผิดพลาดในการโหลดข้อมูล'
  } finally {
    loading.value = false
  }
}

const searchTracking = async () => {
  if (!searchTrackingNumber.value) return

  searching.value = true
  await fetchTracking(searchTrackingNumber.value)
  
  // Update URL
  if (tracking.value) {
    await navigateTo(`/tracking/${searchTrackingNumber.value}`, { replace: true })
  }
  
  searching.value = false
}

// Lifecycle
onMounted(() => {
  if (trackingNumber.value) {
    searchTrackingNumber.value = trackingNumber.value
    fetchTracking()
  }
})

// Head
useHead({
  title: computed(() => 
    tracking.value 
      ? `ติดตามสินค้า ${tracking.value.tracking_number} - ShopHub`
      : 'ติดตามการจัดส่ง - ShopHub'
  )
})
</script>
