<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
          </div>
          
          <nav class="hidden md:flex space-x-8">
            <NuxtLink to="/" class="text-gray-300 hover:text-white transition-colors">หน้าแรก</NuxtLink>
            <NuxtLink to="/products" class="text-gray-300 hover:text-white transition-colors">สินค้า</NuxtLink>
            <NuxtLink to="/categories" class="text-white font-semibold">หมวดหมู่</NuxtLink>
            <NuxtLink to="/about" class="text-gray-300 hover:text-white transition-colors">เกี่ยวกับเรา</NuxtLink>
            <NuxtLink to="/contact" class="text-gray-300 hover:text-white transition-colors">ติดต่อ</NuxtLink>
          </nav>
          
          <div class="flex items-center space-x-4">
            <!-- Cart Icon -->
            <NuxtLink
              to="/cart"
              class="relative text-gray-300 hover:text-white transition-colors p-2"
              title="ตะกร้าสินค้า"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0H17"></path>
              </svg>
              <!-- Cart Count Badge -->
              <span 
                v-if="cartCount > 0" 
                class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
              >
                {{ cartCount > 99 ? '99+' : cartCount }}
              </span>
            </NuxtLink>
            
            <!-- Show ProfileDropdown if logged in, otherwise show Login/Register buttons -->
            <ProfileDropdown v-if="isLoggedIn" :user="currentUser" @logout="handleLogout" />
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

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-white mb-4">หมวดหมู่สินค้า</h1>
        <p class="text-xl text-gray-300">เลือกซื้อสินค้าตามหมวดหมู่ที่คุณสนใจ</p>
      </div>

      <!-- Categories Grid -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-300">กำลังโหลดหมวดหมู่...</p>
      </div>

      <div v-else-if="categories.length === 0" class="text-center py-12">
        <p class="text-xl text-gray-300">ไม่พบหมวดหมู่สินค้า</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <div
          v-for="category in categories"
          :key="category.id"
          class="bg-black border border-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform duration-300 cursor-pointer hover:border-white"
          @click="viewCategory(category.slug)"
        >
          <!-- Category Image -->
          <div class="h-48 bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
            <div v-if="category.image_url" class="w-full h-full bg-cover bg-center" :style="{ backgroundImage: `url(${category.image_url})` }"></div>
            <svg v-else class="w-20 h-20 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          
          <!-- Category Info -->
          <div class="p-6">
            <h3 class="text-xl font-semibold text-white mb-3 text-center">{{ category.name }}</h3>
            <p class="text-gray-400 text-sm mb-4 text-center line-clamp-2">{{ category.description }}</p>
            
            <!-- Product Count -->
            <div class="text-center">
              <span class="text-white font-semibold">{{ category.product_count }}</span>
              <span class="text-gray-400 ml-1">สินค้า</span>
            </div>
            
            <!-- View Button -->
            <div class="mt-4 text-center">
              <button class="bg-white text-black px-6 py-2 rounded-md hover:bg-gray-200 transition-colors w-full">
                ดูสินค้า
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Featured Categories Section -->
      <div v-if="categories.length > 0" class="mt-20">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-white mb-4">หมวดหมู่ทั้งหมด</h2>
          <p class="text-lg text-gray-300">ค้นพบหมวดหมู่สินค้าที่หลากหลาย</p>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div v-for="category in categories.slice(0, 4)" :key="category.id" 
               class="bg-black border border-gray-800 rounded-lg p-8 hover:transform hover:scale-105 transition-transform duration-300 cursor-pointer"
               @click="viewCategory(category.slug)">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mr-6">
                <svg class="w-8 h-8 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div>
                <h3 class="text-2xl font-bold text-white">{{ category.name }}</h3>
                <p class="text-gray-300">{{ category.description || 'หมวดหมู่สินค้าคุณภาพ' }}</p>
              </div>
            </div>
            <p class="text-gray-400 mb-6">{{ category.description || 'อัพเดทสินค้าใหม่ล่าสุด พร้อมคุณภาพและราคาที่เป็นมิตร' }}</p>
            <button class="bg-white text-black px-6 py-3 rounded-md font-semibold hover:bg-gray-200 transition-colors">
              ดูสินค้า
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-black border-t border-gray-800 mt-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="text-center">
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

// Import ProfileDropdown component
import ProfileDropdown from '~/components/ProfileDropdown.vue'

const { apiCall } = useApi()
const { cartCount, getCartCount } = useCart()

// Reactive data
const categories = ref([])
const loading = ref(true)

// Authentication state
const isLoggedIn = ref(false)
const currentUser = ref(null)

// Check authentication status
const checkAuthStatus = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    isLoggedIn.value = true
    currentUser.value = JSON.parse(user)
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

const fetchCategories = async () => {
  try {
    loading.value = true
    const response = await apiCall('/api/categories')
    
    if (response.success) {
      categories.value = response.categories
    }
  } catch (error) {
    console.error('Error fetching categories:', error)
  } finally {
    loading.value = false
  }
}

const viewCategory = (slug) => {
  navigateTo(`/categories/${slug}`)
}

// Lifecycle
onMounted(async () => {
  await fetchCategories()
  checkAuthStatus() // Check authentication status on mount
  getCartCount() // Get cart count on mount
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar */
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
