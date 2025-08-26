<template>
  <div class="min-h-screen bg-black flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-white">
          สร้างบัญชีใหม่
        </h2>
        <p v-if="isFirstTimeUser" class="mt-2 text-sm text-green-400 mb-4">
          🎉 ยินดีต้อนรับสู่ ShopHub! เริ่มต้นการเดินทางของคุณที่นี่
        </p>
        <p class="mt-2 text-sm text-gray-300">
          หรือ
          <NuxtLink to="/login" class="font-medium text-white hover:text-gray-200 underline">
            เข้าสู่ระบบ
          </NuxtLink>
        </p>
      </div>

      <!-- Register Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <!-- First Name Field -->
          <div>
            <label for="first_name" class="block text-sm font-medium text-white">
              ชื่อ
            </label>
            <input
              id="first_name"
              v-model="form.first_name"
              name="first_name"
              type="text"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
              placeholder="กรอกชื่อ"
            />
          </div>

          <!-- Last Name Field -->
          <div>
            <label for="last_name" class="block text-sm font-medium text-white">
              นามสกุล
            </label>
            <input
              id="last_name"
              v-model="form.last_name"
              name="last_name"
              type="text"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
              placeholder="กรอกนามสกุล"
            />
          </div>

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
              placeholder="กรอกชื่อผู้ใช้ (อย่างน้อย 3 ตัวอักษร)"
            />
            <p class="mt-1 text-xs text-gray-400">ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร</p>
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
              placeholder="กรอกรหัสผ่าน (อย่างน้อย 6 ตัวอักษร)"
            />
            <p class="mt-1 text-xs text-gray-400">รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร</p>
          </div>

          <!-- Confirm Password Field -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-white">
              ยืนยันรหัสผ่าน
            </label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              name="confirmPassword"
              type="password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
              placeholder="กรอกรหัสผ่านอีกครั้ง"
            />
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="text-red-400 text-sm text-center bg-red-900 bg-opacity-20 p-3 rounded-md">
          {{ error }}
        </div>

        <!-- Success Message -->
        <div v-if="success" class="text-green-400 text-sm text-center bg-green-900 bg-opacity-20 p-3 rounded-md">
          {{ success }}
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
            {{ loading ? 'กำลังสร้างบัญชี...' : 'สร้างบัญชี' }}
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
  first_name: '',
  last_name: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')
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

const validateForm = () => {
  // ตรวจสอบความยาว username
  if (form.value.username.length < 3) {
    error.value = 'ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร'
    return false
  }

  // ตรวจสอบความยาวรหัสผ่าน
  if (form.value.password.length < 6) {
    error.value = 'รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร'
    return false
  }

  // ตรวจสอบการยืนยันรหัสผ่าน
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'รหัสผ่านไม่ตรงกัน'
    return false
  }

  return true
}

const handleRegister = async () => {
  error.value = ''
  success.value = ''

  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    const response = await apiCall('/api/register', {
      method: 'POST',
      body: {
        first_name: form.value.first_name,
        last_name: form.value.last_name,
        username: form.value.username,
        password: form.value.password
      }
    })

    success.value = 'สร้างบัญชีสำเร็จ! กำลังไปยังหน้าเข้าสู่ระบบ...'
    
    // รีเซ็ตฟอร์ม
    form.value = {
      first_name: '',
      last_name: '',
      username: '',
      password: '',
      confirmPassword: ''
    }

    // ไปยังหน้า login หลังจาก 2 วินาที
    setTimeout(async () => {
      await navigateTo('/login')
    }, 2000)

  } catch (err) {
    console.error('Register error:', err)
    if (err.data?.error) {
      error.value = err.data.error
    } else {
      error.value = 'เกิดข้อผิดพลาดในการสร้างบัญชี'
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
