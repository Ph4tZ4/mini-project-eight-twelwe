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
            <NuxtLink to="/products" class="text-white font-semibold">สินค้า</NuxtLink>
            <NuxtLink to="/categories" class="text-gray-300 hover:text-white transition-colors">หมวดหมู่</NuxtLink>
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
        <h1 class="text-4xl font-bold text-white mb-4">สินค้าทั้งหมด</h1>
        <p class="text-xl text-gray-300">ค้นพบสินค้าคุณภาพสูงที่คุณต้องการ</p>
      </div>

      <!-- Filters and Search -->
      <div class="bg-black border border-gray-800 rounded-lg p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="md:col-span-2">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="ค้นหาสินค้า..."
              class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white"
              @input="handleSearch"
            />
          </div>
          
          <!-- Category Filter -->
          <div>
            <select
              v-model="selectedCategory"
              @change="handleCategoryChange"
              class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:border-white"
            >
              <option value="">ทุกหมวดหมู่</option>
              <option
                v-for="category in categories"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>
          
          <!-- Sort -->
          <div>
            <select
              v-model="sortBy"
              @change="handleSortChange"
              class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:border-white"
            >
              <option value="created_at">ใหม่ล่าสุด</option>
              <option value="price">ราคา</option>
              <option value="name">ชื่อสินค้า</option>
              <option value="rating">คะแนน</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Products Grid -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-300">กำลังโหลดสินค้า...</p>
      </div>

      <div v-else-if="products.length === 0" class="text-center py-12">
        <p class="text-xl text-gray-300">ไม่พบสินค้าที่ค้นหา</p>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="product in products"
            :key="product.id"
            class="bg-black border border-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform duration-300 cursor-pointer"
            @click="viewProduct(product.id)"
          >
            <!-- Product Image -->
            <div class="h-64 bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
              <svg class="w-20 h-20 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            
            <!-- Product Info -->
            <div class="p-6">
              <h3 class="text-lg font-semibold text-white mb-2 line-clamp-2">{{ product.name }}</h3>
              <p class="text-gray-400 text-sm mb-4 line-clamp-2">{{ product.description }}</p>
              
              <!-- Price -->
              <div class="flex items-center justify-between mb-4">
                <div>
                  <span class="text-2xl font-bold text-white">฿{{ formatPrice(product.price) }}</span>
                  <span v-if="product.original_price && product.original_price > product.price" class="text-gray-400 line-through ml-2">
                    ฿{{ formatPrice(product.original_price) }}
                  </span>
                </div>
                <span v-if="product.stock_quantity > 0" class="text-green-400 text-sm">มีสินค้า</span>
                <span v-else class="text-red-400 text-sm">หมดสินค้า</span>
              </div>
              
              <!-- Rating -->
              <div class="flex items-center mb-4">
                <div class="flex text-yellow-400">
                  <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= product.rating ? 'text-yellow-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
                <span class="text-gray-400 text-sm ml-2">({{ product.review_count }})</span>
              </div>
              
              <!-- View Details Button -->
              <div class="flex justify-center">
                <button 
                  class="bg-white text-black px-6 py-2 rounded-md hover:bg-gray-200 transition-colors flex items-center gap-2 w-full justify-center"
                  @click.stop="viewProduct(product.id)"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                  ดูรายละเอียด
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total_pages > 1" class="mt-12 flex justify-center">
          <div class="flex space-x-2">
            <button
              v-for="page in pagination.total_pages"
              :key="page"
              @click="goToPage(page)"
              :class="[
                'px-4 py-2 rounded-md transition-colors',
                page === pagination.page
                  ? 'bg-white text-black'
                  : 'bg-gray-800 text-white hover:bg-gray-700'
              ]"
            >
              {{ page }}
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
const products = ref([])
const categories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('created_at')
const pagination = ref({
  page: 1,
  limit: 12,
  total_products: 0,
  total_pages: 0
})

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

// Debounced search
let searchTimeout

const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    pagination.value.page = 1
    fetchProducts()
  }, 500)
}

const handleCategoryChange = () => {
  pagination.value.page = 1
  fetchProducts()
}

const handleSortChange = () => {
  pagination.value.page = 1
  fetchProducts()
}

const goToPage = (page) => {
  pagination.value.page = page
  fetchProducts()
}

const fetchProducts = async () => {
  try {
    loading.value = true
    
    const params = new URLSearchParams({
      page: pagination.value.page.toString(),
      limit: pagination.value.limit.toString(),
      sort_by: sortBy.value,
      sort_order: 'desc'
    })
    
    if (selectedCategory.value) {
      params.append('category', selectedCategory.value)
    }
    
    if (searchQuery.value) {
      params.append('search', searchQuery.value)
    }
    
    const response = await apiCall(`/api/products?${params}`)
    
    if (response.success) {
      products.value = response.products
      pagination.value = response.pagination
    }
  } catch (error) {
    console.error('Error fetching products:', error)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await apiCall('/api/categories')
    if (response.success) {
      categories.value = response.categories
    }
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

const viewProduct = (productId) => {
  navigateTo(`/products/${productId}`)
}

const formatPrice = (price) => {
  return price.toLocaleString('th-TH')
}

// Lifecycle
onMounted(async () => {
  await Promise.all([fetchProducts(), fetchCategories()])
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
