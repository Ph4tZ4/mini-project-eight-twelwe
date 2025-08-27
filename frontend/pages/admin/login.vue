<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8">
      <div class="bg-white shadow-lg rounded-lg p-8">
        <div class="text-center">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Admin Login</h2>
          <p class="text-gray-600">เข้าสู่ระบบผู้ดูแล</p>
        </div>

        <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              ชื่อผู้ใช้
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
              placeholder="กรอกชื่อผู้ใช้"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              รหัสผ่าน
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
              placeholder="กรอกรหัสผ่าน"
            />
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3">
            <p class="text-red-600 text-sm">{{ error }}</p>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg
              v-if="loading"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{ loading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <NuxtLink
            to="/login"
            class="text-sm text-gray-600 hover:text-black"
          >
            ← กลับไปหน้าเข้าสู่ระบบผู้ใช้
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Meta tags
useHead({
  title: 'Admin Login - ShopHub',
  meta: [
    { name: 'description', content: 'Admin login page for ShopHub management system' }
  ]
})

// Define page meta
definePageMeta({
  layout: false,
  middleware: 'guest'
})

// Reactive state
const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

// Composables
const { apiCall } = useApi()
const router = useRouter()

// Methods
const handleLogin = async () => {
  loading.value = true
  error.value = ''

  console.log('Attempting login with:', form)

  try {
    // Use direct $fetch instead of apiCall for debugging
    const response = await $fetch('http://localhost:5550/api/admin/login', {
      method: 'POST',
      body: JSON.stringify(form),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    console.log('Login response:', response)

    if (response.access_token) {
      // Store token and user data
      const token = useCookie('auth-token', {
        default: () => null,
        httpOnly: false,
        secure: false,
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 7 // 7 days
      })
      
      const user = useCookie('auth-user', {
        default: () => null,
        httpOnly: false,
        secure: false,
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 7 // 7 days
      })

      token.value = response.access_token
      user.value = response.user

      console.log('Stored token and user, redirecting...')

      // Redirect to admin dashboard
      await router.push('/admin/dashboard')
    }
  } catch (err) {
    console.error('Admin login error:', err)
    console.error('Error details:', err.data || err.response)
    
    // Extract meaningful error message
    let errorMessage = 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ'
    
    if (err.data && err.data.error) {
      errorMessage = err.data.error
    } else if (err.statusMessage) {
      errorMessage = err.statusMessage
    } else if (err.message) {
      errorMessage = err.message
    }
    
    error.value = errorMessage
  } finally {
    loading.value = false
  }
}

// Auto-focus on username field
onMounted(() => {
  const usernameInput = document.getElementById('username')
  if (usernameInput) {
    usernameInput.focus()
  }
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
