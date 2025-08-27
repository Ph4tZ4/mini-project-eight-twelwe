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
            <h1 class="text-2xl font-bold text-gray-900">ข้อความติดต่อ</h1>
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
        </svg>
        <h2 class="text-2xl font-bold text-gray-900 mb-2">ข้อความติดต่อ</h2>
        <p class="text-gray-600 mb-6">หน้านี้จะแสดงข้อความติดต่อจากลูกค้าและอนุญาตให้คุณตอบกลับ</p>
        <div class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <p class="text-yellow-800 text-sm">🚧 หน้านี้อยู่ระหว่างการพัฒนา</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
useHead({
  title: 'ข้อความติดต่อ - Admin Dashboard'
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
