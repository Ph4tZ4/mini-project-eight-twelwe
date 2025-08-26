<template>
  <header class="bg-black border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>

        <nav class="hidden md:flex space-x-8">
          <NuxtLink to="/home" class="text-gray-300 hover:text-white transition-colors">หน้าแรก</NuxtLink>
          <NuxtLink to="/products" class="text-gray-300 hover:text-white transition-colors">สินค้า</NuxtLink>
          <NuxtLink to="/categories" class="text-gray-300 hover:text-white transition-colors">หมวดหมู่</NuxtLink>
          <NuxtLink to="/about" class="text-gray-300 hover:text-white transition-colors">เกี่ยวกับเรา</NuxtLink>
          <NuxtLink to="/contact" class="text-gray-300 hover:text-white transition-colors">ติดต่อ</NuxtLink>
        </nav>

        <div class="flex items-center gap-4">
          <NuxtLink to="/cart" class="relative inline-flex items-center justify-center w-10 h-10 rounded-full border border-gray-700 hover:border-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 text-white">
              <path d="M2.25 3a.75.75 0 000 1.5h1.386c.17 0 .318.114.36.279l2.558 9.834A2.25 2.25 0 008.737 16.5h8.764a2.25 2.25 0 002.183-1.653l1.557-5.672A.75.75 0 0020.5 8.5H7.214l-.6-2.308A2.25 2.25 0 004.996 4.5H2.25z" />
              <path d="M8.25 20.25a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM18.75 20.25a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
            </svg>
            <span v-if="totals.total_quantity > 0" class="absolute -top-1 -right-1 bg-white text-black text-xs font-bold rounded-full px-1.5 py-0.5">
              {{ totals.total_quantity }}
            </span>
          </NuxtLink>

          <ProfileDropdown v-if="isLoggedIn" :user="currentUser" @logout="handleLogout" />
          <template v-else>
            <NuxtLink to="/login" class="text-gray-300 hover:text-white transition-colors">เข้าสู่ระบบ</NuxtLink>
            <NuxtLink to="/register" class="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">สมัครสมาชิก</NuxtLink>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import ProfileDropdown from '~/components/ProfileDropdown.vue'
const { isAuthenticated, getCurrentUser } = useApi()
const { totals, fetchCart } = useCart()

const isLoggedIn = ref(false)
const currentUser = ref(null)

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isLoggedIn.value = false
  currentUser.value = null
  fetchCart()
  navigateTo('/login')
}

onMounted(() => {
  isLoggedIn.value = isAuthenticated()
  currentUser.value = getCurrentUser()
  fetchCart()
  window.addEventListener('storage', () => {
    isLoggedIn.value = isAuthenticated()
    currentUser.value = getCurrentUser()
    fetchCart()
  })
})

onUnmounted(() => {
  window.removeEventListener('storage', () => {})
})
</script>
