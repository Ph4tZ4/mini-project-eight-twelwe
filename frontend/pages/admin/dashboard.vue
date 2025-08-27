<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">
              สวัสดี, {{ user?.username || 'Admin' }}
            </span>
            <button
              @click="logout"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              ออกจากระบบ
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
        <p class="text-red-600">{{ error }}</p>
        <button
          @click="fetchDashboardData"
          class="mt-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm"
        >
          ลองใหม่
        </button>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- Users Stats -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">ผู้ใช้ทั้งหมด</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats?.users?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
              <div class="mt-4">
                <div class="text-sm text-gray-600">
                  ใหม่วันนี้: {{ stats?.users?.new_today || 0 }} | 
                  เดือนนี้: {{ stats?.users?.new_this_month || 0 }}
                </div>
              </div>
            </div>
          </div>

          <!-- Products Stats -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 2L3 7v11a2 2 0 002 2h10a2 2 0 002-2V7l-7-5zM8 12a2 2 0 114 0v2H8v-2z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">สินค้าทั้งหมด</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats?.products?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
              <div class="mt-4">
                <div class="text-sm text-gray-600">
                  เปิดขาย: {{ stats?.products?.active || 0 }} | 
                  หมด: {{ stats?.products?.out_of_stock || 0 }}
                </div>
              </div>
            </div>
          </div>

          <!-- Orders Stats -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">คำสั่งซื้อทั้งหมด</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats?.orders?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
              <div class="mt-4">
                <div class="text-sm text-gray-600">
                  วันนี้: {{ stats?.orders?.today || 0 }} | 
                  รอดำเนินการ: {{ stats?.orders?.pending || 0 }}
                </div>
              </div>
            </div>
          </div>

          <!-- Revenue Stats -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.51-1.31c-.562-.649-1.413-1.076-2.353-1.253V5z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">รายได้รวม</dt>
                    <dd class="text-lg font-medium text-gray-900">฿{{ formatCurrency(stats?.revenue?.total || 0) }}</dd>
                  </dl>
                </div>
              </div>
              <div class="mt-4">
                <div class="text-sm text-gray-600">
                  วันนี้: ฿{{ formatCurrency(stats?.revenue?.today || 0) }} | 
                  เดือนนี้: ฿{{ formatCurrency(stats?.revenue?.this_month || 0) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Recent Orders -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                สถานะคำสั่งซื้อ
              </h3>
              <div class="space-y-3">
                <div class="flex justify-between items-center p-3 bg-yellow-50 rounded-lg">
                  <span class="text-sm font-medium text-yellow-800">รอดำเนินการ</span>
                  <span class="text-sm font-bold text-yellow-900">{{ stats?.orders?.pending || 0 }}</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                  <span class="text-sm font-medium text-blue-800">ยืนยันแล้ว</span>
                  <span class="text-sm font-bold text-blue-900">{{ stats?.orders?.confirmed || 0 }}</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                  <span class="text-sm font-medium text-purple-800">จัดส่งแล้ว</span>
                  <span class="text-sm font-bold text-purple-900">{{ stats?.orders?.shipped || 0 }}</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                  <span class="text-sm font-medium text-green-800">ส่งมอบแล้ว</span>
                  <span class="text-sm font-bold text-green-900">{{ stats?.orders?.delivered || 0 }}</span>
                </div>
              </div>
              <div class="mt-4">
                <NuxtLink
                  to="/admin/orders"
                  class="text-sm text-blue-600 hover:text-blue-500 font-medium"
                >
                  ดูคำสั่งซื้อทั้งหมด →
                </NuxtLink>
              </div>
            </div>
          </div>

          <!-- Contact Messages -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                ข้อความติดต่อ
              </h3>
              <div class="space-y-3">
                <div class="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                  <span class="text-sm font-medium text-red-800">ยังไม่อ่าน</span>
                  <span class="text-sm font-bold text-red-900">{{ stats?.contacts?.unread || 0 }}</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span class="text-sm font-medium text-gray-800">ทั้งหมด</span>
                  <span class="text-sm font-bold text-gray-900">{{ stats?.contacts?.total || 0 }}</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                  <span class="text-sm font-medium text-blue-800">รถเข็นที่มีสินค้า</span>
                  <span class="text-sm font-bold text-blue-900">{{ stats?.carts?.active || 0 }}</span>
                </div>
              </div>
              <div class="mt-4">
                <NuxtLink
                  to="/admin/contacts"
                  class="text-sm text-blue-600 hover:text-blue-500 font-medium"
                >
                  ดูข้อความทั้งหมด →
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <NuxtLink
            to="/admin/users"
            class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">จัดการผู้ใช้</h3>
                <p class="text-sm text-gray-500">ดูและจัดการบัญชีผู้ใช้</p>
              </div>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/admin/orders"
            class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 bg-yellow-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">จัดการคำสั่งซื้อ</h3>
                <p class="text-sm text-gray-500">ดูและอัปเดตคำสั่งซื้อ</p>
              </div>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/admin/products"
            class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 2L3 7v11a2 2 0 002 2h10a2 2 0 002-2V7l-7-5zM8 12a2 2 0 114 0v2H8v-2z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">จัดการสินค้า</h3>
                <p class="text-sm text-gray-500">เพิ่ม แก้ไข และลบสินค้า</p>
              </div>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/admin/contacts"
            class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">ข้อความติดต่อ</h3>
                <p class="text-sm text-gray-500">ดูและตอบข้อความติดต่อ</p>
              </div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// Meta tags
useHead({
  title: 'Admin Dashboard - ShopHub',
  meta: [
    { name: 'description', content: 'Admin dashboard for ShopHub management system' }
  ]
})

// Define page meta
definePageMeta({
  layout: false,
  middleware: 'admin-auth'
})

// Reactive state
const stats = ref(null)
const loading = ref(true)
const error = ref('')

// Composables
const { apiCall } = useApi()
const router = useRouter()

// Get user from cookie
const user = useCookie('auth-user')

// Methods
const fetchDashboardData = async () => {
  loading.value = true
  error.value = ''

  try {
    const token = useCookie('auth-token')
    
    const response = await apiCall('/api/admin/dashboard/stats', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })

    stats.value = response
  } catch (err) {
    console.error('Dashboard error:', err)
    error.value = err.message || 'เกิดข้อผิดพลาดในการโหลดข้อมูล'
  } finally {
    loading.value = false
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('th-TH', {
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const logout = () => {
  // Clear auth data
  const token = useCookie('auth-token')
  const userData = useCookie('auth-user')
  
  token.value = null
  userData.value = null
  
  // Redirect to admin login
  router.push('/admin/login')
}

// Fetch data on component mount
onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
