<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <NuxtLink 
              to="/admin/dashboard"
              class="text-gray-500 hover:text-gray-700"
            >
              ← Dashboard
            </NuxtLink>
            <h1 class="text-2xl font-bold text-gray-900">จัดการสินค้า</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">{{ user?.username || 'Admin' }}</span>
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
      <div class="bg-white shadow rounded-lg p-8 text-center">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
        <h2 class="text-2xl font-bold text-gray-900 mb-2">จัดการสินค้า</h2>
        <p class="text-gray-600 mb-6">หน้านี้จะแสดงรายการสินค้าทั้งหมดและอนุญาตให้คุณเพิ่ม แก้ไข และลบสินค้า</p>
        <div class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <p class="text-yellow-800 text-sm">🚧 หน้านี้อยู่ระหว่างการพัฒนา</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
useHead({
  title: 'จัดการสินค้า - Admin Dashboard'
})

definePageMeta({
  layout: false,
  middleware: 'admin-auth'
})

const user = useCookie('auth-user')
const router = useRouter()

const logout = () => {
  const token = useCookie('auth-token')
  const userData = useCookie('auth-user')
  token.value = null
  userData.value = null
  router.push('/admin/login')
}
</script>
