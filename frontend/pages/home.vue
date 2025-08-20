<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header/Navigation -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- Logo -->
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-white">ShopHub</h1>
          </div>
          
          <!-- Navigation -->
          <nav class="hidden md:flex space-x-8">
            <NuxtLink to="/home" class="text-white font-semibold">หน้าแรก</NuxtLink>
            <NuxtLink to="/products" class="text-gray-300 hover:text-white transition-colors">สินค้า</NuxtLink>
            <NuxtLink to="/categories" class="text-gray-300 hover:text-white transition-colors">หมวดหมู่</NuxtLink>
            <NuxtLink to="/about" class="text-gray-300 hover:text-white transition-colors">เกี่ยวกับเรา</NuxtLink>
            <NuxtLink to="/contact" class="text-gray-300 hover:text-white transition-colors">ติดต่อ</NuxtLink>
          </nav>
          
          <!-- Auth Buttons -->
          <div class="flex items-center space-x-4">
            <!-- Show ProfileDropdown when user is logged in -->
            <ProfileDropdown v-if="isLoggedIn" :user="currentUser" @logout="handleLogout" />
            
            <!-- Show Login/Register buttons when user is not logged in -->
            <template v-else>
              <NuxtLink
                to="/login"
                class="text-gray-300 hover:text-white transition-colors"
              >
                เข้าสู่ระบบ
              </NuxtLink>
              <NuxtLink
                to="/register"
                class="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors"
              >
                สมัครสมาชิก
              </NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section id="home" class="relative overflow-hidden bg-gradient-to-br from-gray-900 to-black py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
            ช้อปปิ้งออนไลน์
            <span class="block text-white">ที่คุณไว้วางใจ</span>
          </h1>
          <p class="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            ค้นพบสินค้าคุณภาพสูง ราคาเป็นมิตร พร้อมบริการจัดส่งที่รวดเร็วและปลอดภัย
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#products"
              class="bg-white text-black px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-200 transition-colors"
            >
              ดูสินค้าทั้งหมด
            </a>
            <a
              href="#categories"
              class="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-black transition-colors"
            >
              เลือกหมวดหมู่
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Categories -->
    <section id="categories" class="py-20 bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-white mb-4">หมวดหมู่สินค้า</h2>
          <p class="text-xl text-gray-300">เลือกซื้อสินค้าตามหมวดหมู่ที่คุณสนใจ</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <!-- Loading state -->
          <div v-if="loading" class="col-span-full text-center py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
            <p class="text-gray-400 mt-4">กำลังโหลดข้อมูล...</p>
          </div>
          
          <!-- Error state -->
          <div v-else-if="error" class="col-span-full text-center py-8">
            <p class="text-red-400">{{ error }}</p>
            <button @click="fetchHomeData" class="mt-4 bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">
              ลองใหม่
            </button>
          </div>
          
          <!-- Categories -->
          <div v-else v-for="category in homeData.main_categories" :key="category.id" class="bg-black p-6 rounded-lg border border-gray-700 hover:border-white transition-colors group">
            <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white text-center mb-2">{{ category.name }}</h3>
            <p class="text-gray-400 text-center">{{ category.description || 'หมวดหมู่สินค้าคุณภาพ' }}</p>
          </div>
          
          <!-- Fallback categories if no data -->
          <div v-if="!loading && !error && homeData.main_categories.length === 0" class="col-span-full text-center py-8">
            <p class="text-gray-400">ไม่มีข้อมูลหมวดหมู่</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section id="products" class="py-20 bg-black">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-white mb-4">สินค้าแนะนำ</h2>
          <p class="text-xl text-gray-300">สินค้าขายดีที่ลูกค้าเลือกซื้อมากที่สุด</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          <!-- Loading state -->
          <div v-if="loading" class="col-span-full text-center py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
            <p class="text-gray-400 mt-4">กำลังโหลดสินค้า...</p>
          </div>
          
          <!-- Error state -->
          <div v-else-if="error" class="col-span-full text-center py-8">
            <p class="text-red-400">{{ error }}</p>
            <button @click="fetchHomeData" class="mt-4 bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">
              ลองใหม่
            </button>
          </div>
          
          <!-- Products -->
          <div v-else v-for="product in homeData.featured_products" :key="product.id" class="bg-gray-900 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform duration-300">
            <div class="h-64 bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
              <svg class="w-20 h-20 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="p-6">
              <h3 class="text-lg font-semibold text-white mb-2">{{ product.name }}</h3>
              <p class="text-gray-400 text-sm mb-4">{{ product.description || 'สินค้าคุณภาพสูง' }}</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-white">฿{{ product.price?.toLocaleString() || '0' }}</span>
                <button class="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">
                  เพิ่มลงตะกร้า
                </button>
              </div>
            </div>
          </div>
          
          <!-- Fallback products if no data -->
          <div v-if="!loading && !error && homeData.featured_products.length === 0" class="col-span-full text-center py-8">
            <p class="text-gray-400">ไม่มีสินค้าแนะนำ</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-white mb-4">ทำไมต้องเลือกเรา</h2>
          <p class="text-xl text-gray-300">บริการที่เหนือกว่าด้วยคุณภาพและความไว้วางใจ</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-4">จัดส่งฟรี</h3>
            <p class="text-gray-300">จัดส่งฟรีสำหรับออเดอร์เกิน ฿1,000 ทั่วประเทศ</p>
          </div>
          
          <div class="text-center">
            <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-4">รับประกันสินค้า</h3>
            <p class="text-gray-300">รับประกันสินค้าทุกชิ้น 7-30 วัน ตามประเภทสินค้า</p>
          </div>
          
          <div class="text-center">
            <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-4">บริการ 24/7</h3>
            <p class="text-gray-300">บริการลูกค้าตลอด 24 ชั่วโมง พร้อมให้คำปรึกษา</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="py-20 bg-black border-t border-gray-800">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">รับข่าวสารและโปรโมชั่น</h2>
        <p class="text-gray-300 mb-8">สมัครรับข่าวสารเพื่อไม่พลาดโปรโมชั่นพิเศษและสินค้าใหม่</p>
        <div class="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
          <input
            type="email"
            placeholder="กรอกอีเมลของคุณ"
            class="flex-1 px-4 py-3 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white"
          />
          <button class="bg-white text-black px-6 py-3 rounded-md font-semibold hover:bg-gray-200 transition-colors">
            สมัคร
          </button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 border-t border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-xl font-bold text-white mb-4">ShopHub</h3>
            <p class="text-gray-300">เว็บขายของออนไลน์ที่คุณไว้วางใจ พร้อมบริการจัดส่งที่รวดเร็วและปลอดภัย</p>
          </div>
          
          <div>
            <h4 class="text-lg font-semibold text-white mb-4">หมวดหมู่สินค้า</h4>
            <ul class="space-y-2 text-gray-300">
              <li><a href="#" class="hover:text-white transition-colors">อิเล็กทรอนิกส์</a></li>
              <li><a href="#" class="hover:text-white transition-colors">แฟชั่น</a></li>
              <li><a href="#" class="hover:text-white transition-colors">บ้านและไลฟ์สไตล์</a></li>
              <li><a href="#" class="hover:text-white transition-colors">กีฬาและสุขภาพ</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="text-lg font-semibold text-white mb-4">บริการลูกค้า</h4>
            <ul class="space-y-2 text-gray-300">
              <li><a href="#" class="hover:text-white transition-colors">วิธีสั่งซื้อ</a></li>
              <li><a href="#" class="hover:text-white transition-colors">การจัดส่ง</a></li>
              <li><a href="#" class="hover:text-white transition-colors">การคืนสินค้า</a></li>
              <li><a href="#" class="hover:text-white transition-colors">ติดต่อเรา</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="text-lg font-semibold text-white mb-4">ติดต่อเรา</h4>
            <ul class="space-y-2 text-gray-300">
              <li>โทร: 02-123-4567</li>
              <li>อีเมล: info@shophub.com</li>
              <li>ที่อยู่: กรุงเทพมหานคร</li>
            </ul>
          </div>
        </div>
        
        <div class="border-t border-gray-800 mt-8 pt-8 text-center">
          <p class="text-gray-400">&copy; 2024 ShopHub. สงวนลิขสิทธิ์ทั้งหมด.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'default'
})

// Import the ProfileDropdown component
import ProfileDropdown from '~/components/ProfileDropdown.vue'

// ใช้ client-side rendering เพื่อหลีกเลี่ยง hydration mismatch
const isClient = ref(false)

// Authentication state
const isLoggedIn = ref(false)
const currentUser = ref(null)

// Data for the home page
const homeData = ref({
  featured_products: [],
  main_categories: [],
  latest_products: []
})

const loading = ref(true)
const error = ref('')

const { apiCall } = useApi()

// Check authentication status
const checkAuthStatus = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    try {
      currentUser.value = JSON.parse(user)
      isLoggedIn.value = true
    } catch (e) {
      console.error('Error parsing user data:', e)
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  } else {
    isLoggedIn.value = false
    currentUser.value = null
  }
}

// Handle logout event from ProfileDropdown
const handleLogout = () => {
  // Clear authentication state
  isLoggedIn.value = false
  currentUser.value = null
  
  // Clear localStorage
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('hasVisitedBefore')
  
  // Redirect to login page
  navigateTo('/login')
}

// Fetch home page data
const fetchHomeData = async () => {
  try {
    loading.value = true
    const response = await apiCall('/api/home', {
      method: 'GET'
    })
    
    if (response.success) {
      homeData.value = response
    }
  } catch (err) {
    console.error('Error fetching home data:', err)
    error.value = 'เกิดข้อผิดพลาดในการดึงข้อมูล'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  isClient.value = true
  checkAuthStatus()
  fetchHomeData()
  
  // Listen for storage changes (login/logout)
  window.addEventListener('storage', checkAuthStatus)
})

onUnmounted(() => {
  window.removeEventListener('storage', checkAuthStatus)
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

/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}
</style>
