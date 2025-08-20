<template>
  <div class="min-h-screen bg-black flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-white">
          เข้าสู่ระบบ
        </h2>
        <p v-if="isFirstTimeUser" class="mt-2 text-sm text-green-400 mb-4">
          🎉 ยินดีต้อนรับสู่ ShopHub! นี่เป็นการเยี่ยมชมครั้งแรกของคุณ
        </p>
        <p class="mt-2 text-sm text-gray-300">
          หรือ
          <NuxtLink to="/register" class="font-medium text-white hover:text-gray-200 underline">
            สร้างบัญชีใหม่
          </NuxtLink>
        </p>
      </div>

      <!-- Login Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <!-- Username Field -->
          <div>
            <label for="username" class="block text-sm font-medium text-white">
              ชื่อผู้ใช้
            </label>
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
              placeholder="กรอกชื่อผู้ใช้"
            />
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-white">
              รหัสผ่าน
            </label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
              placeholder="กรอกรหัสผ่าน"
            />
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="text-red-400 text-sm text-center bg-red-900 bg-opacity-20 p-3 rounded-md">
          {{ error }}
        </div>

        <!-- Submit Button -->
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-black bg-white hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ loading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
          </button>
        </div>
      </form>

      <!-- Back to Home -->
      <div class="text-center">
        <NuxtLink to="/" class="text-gray-400 hover:text-white text-sm">
          ← กลับหน้าหลัก
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'default'
})

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const isFirstTimeUser = ref(false)

const { apiCall } = useApi()

// Check if this is the user's first visit
const checkFirstTimeUser = () => {
  const hasVisitedBefore = localStorage.getItem('hasVisitedBefore')
  if (!hasVisitedBefore) {
    isFirstTimeUser.value = true
    // Mark as visited
    localStorage.setItem('hasVisitedBefore', 'true')
  }
}

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    error.value = 'กรุณากรอกข้อมูลให้ครบถ้วน'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await apiCall('/api/login', {
      method: 'POST',
      body: {
        username: form.value.username,
        password: form.value.password
      }
    })

    // บันทึก token และข้อมูลผู้ใช้
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))

    // ไปยังหน้าหลัก
    await navigateTo('/home')

  } catch (err) {
    console.error('Login error:', err)
    if (err.data?.error) {
      error.value = err.data.error
    } else {
      error.value = 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ'
    }
  } finally {
    loading.value = false
  }
}

// Disable scrolling when component mounts
onMounted(() => {
  document.body.style.overflow = 'hidden'
  checkFirstTimeUser()
})

// Re-enable scrolling when component unmounts
onUnmounted(() => {
  document.body.style.overflow = 'auto'
})
</script>

<style scoped>
/* Disable scrolling for the entire page */
:deep(body) {
  overflow: hidden !important;
}

/* Ensure the page takes full height without scrolling */
.min-h-screen {
  min-height: 100vh;
  height: 100vh;
}

/* Custom scrollbar for webkit browsers - disabled for this page */
::-webkit-scrollbar {
  display: none;
}
</style>
