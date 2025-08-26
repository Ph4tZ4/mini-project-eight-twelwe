<template>
  <div class="min-h-screen bg-black text-white">
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
            <ProfileDropdown v-if="isLoggedIn" :user="currentUser" @logout="handleLogout" />
            <template v-else>
              <NuxtLink to="/login" class="text-gray-300 hover:text-white transition-colors">เข้าสู่ระบบ</NuxtLink>
              <NuxtLink to="/register" class="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">สมัครสมาชิก</NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-300">กำลังโหลดสินค้า...</p>
      </div>

      <div v-else-if="!product" class="text-center py-12">
        <p class="text-xl text-gray-300">ไม่พบนสินค้า</p>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="bg-black border border-gray-800 rounded-lg overflow-hidden flex items-center justify-center h-96">
          <img v-if="product.images && product.images.length" :src="product.images[0]" alt="Product image" class="h-full object-contain" />
          <div v-else class="h-full w-full bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
            <svg class="w-20 h-20 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>

        <div>
          <h1 class="text-3xl font-bold mb-4">{{ product.name }}</h1>
          <div class="flex items-center mb-4">
            <div class="flex text-yellow-400 mr-2">
              <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= product.rating ? 'text-yellow-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <span class="text-gray-400">({{ product.review_count }})</span>
          </div>

          <div class="mb-6">
            <span class="text-3xl font-bold">฿{{ formatPrice(product.price) }}</span>
            <span v-if="product.original_price && product.original_price > product.price" class="text-gray-400 line-through ml-3">฿{{ formatPrice(product.original_price) }}</span>
          </div>

          <p class="text-gray-300 mb-6">{{ product.description }}</p>

          <div class="flex items-center space-x-4 mb-8">
            <span v-if="product.stock_quantity > 0" class="text-green-400">มีสินค้า</span>
            <span v-else class="text-red-400">หมดสินค้า</span>
            <span class="text-gray-400">SKU: {{ product.sku }}</span>
            <span v-if="product.brand" class="text-gray-400">Brand: {{ product.brand }}</span>
          </div>

          <div class="flex space-x-4">
            <button class="bg-white text-black px-6 py-3 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" :disabled="product.stock_quantity === 0" @click="addToCart(product)">
              {{ product.stock_quantity > 0 ? 'เพิ่มลงตะกร้า' : 'หมดสินค้า' }}
            </button>
            <NuxtLink to="/products" class="px-6 py-3 rounded-md border border-gray-700 hover:bg-gray-800 transition-colors">กลับไปหน้าสินค้า</NuxtLink>
          </div>
        </div>
      </div>
    </main>

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

import ProfileDropdown from '~/components/ProfileDropdown.vue'

const route = useRoute()
const { apiCall } = useApi()

const product = ref(null)
const loading = ref(true)

// Auth state (match products.vue pattern)
const isLoggedIn = ref(false)
const currentUser = ref(null)

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

const handleLogout = () => {
  isLoggedIn.value = false
  currentUser.value = null
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('hasVisitedBefore')
  navigateTo('/login')
}

const fetchProduct = async () => {
  try {
    loading.value = true
    const id = route.params.id
    const response = await apiCall(`/api/products/${id}`)
    if (response.success) {
      product.value = response.product
    } else {
      product.value = null
    }
  } catch (error) {
    console.error('Error fetching product:', error)
    product.value = null
  } finally {
    loading.value = false
  }
}

const addToCart = (p) => {
  alert(`เพิ่ม ${p.name} ลงตะกร้าแล้ว`)
}

const formatPrice = (price) => {
  return price.toLocaleString('th-TH')
}

onMounted(async () => {
  await fetchProduct()
  checkAuthStatus()
})
</script>

<style scoped>
/* Reuse any local styles if needed */
</style>
