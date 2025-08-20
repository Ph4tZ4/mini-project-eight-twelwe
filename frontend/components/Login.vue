<template>
  <div class="bg-black p-8 rounded-lg border border-gray-700">
    <!-- Header -->
    <div class="text-center mb-8">
      <h2 class="text-3xl font-extrabold text-white">
        เข้าสู่ระบบ
      </h2>
      <p class="mt-2 text-sm text-gray-300">
        หรือ
        <button @click="showRegister = true" class="font-medium text-white hover:text-gray-200 underline">
          สร้างบัญชีใหม่
        </button>
      </p>
    </div>

    <!-- Login Form -->
    <form v-if="!showRegister" class="space-y-6" @submit.prevent="handleLogin">
      <div class="space-y-4">
        <!-- Username Field -->
        <div>
          <label for="username" class="block text-sm font-medium text-white">
            ชื่อผู้ใช้
          </label>
          <input
            id="username"
            v-model="loginForm.username"
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
            v-model="loginForm.password"
            name="password"
            type="password"
            required
            class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
            placeholder="กรอกรหัสผ่าน"
          />
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="loginError" class="text-red-400 text-sm text-center bg-red-900 bg-opacity-20 p-3 rounded-md">
        {{ loginError }}
      </div>

      <!-- Submit Button -->
      <div>
        <button
          type="submit"
          :disabled="loginLoading"
          class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-black bg-white hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
        >
          <span v-if="loginLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
            <svg class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          {{ loginLoading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
        </button>
      </div>
    </form>

    <!-- Register Form -->
    <form v-else class="space-y-6" @submit.prevent="handleRegister">
      <div class="space-y-4">
        <!-- Username Field -->
        <div>
          <label for="reg-username" class="block text-sm font-medium text-white">
            ชื่อผู้ใช้
          </label>
          <input
            id="reg-username"
            v-model="registerForm.username"
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
          <label for="reg-password" class="block text-sm font-medium text-white">
            รหัสผ่าน
          </label>
          <input
            id="reg-password"
            v-model="registerForm.password"
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
          <label for="reg-confirmPassword" class="block text-sm font-medium text-white">
            ยืนยันรหัสผ่าน
          </label>
          <input
            id="reg-confirmPassword"
            v-model="registerForm.confirmPassword"
            name="confirmPassword"
            type="password"
            required
            class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
            placeholder="กรอกรหัสผ่านอีกครั้ง"
          />
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="registerError" class="text-red-400 text-sm text-center bg-red-900 bg-opacity-20 p-3 rounded-md">
        {{ registerError }}
      </div>

      <!-- Success Message -->
      <div v-if="registerSuccess" class="text-green-400 text-sm text-center bg-green-900 bg-opacity-20 p-3 rounded-md">
        {{ registerSuccess }}
      </div>

      <!-- Submit Button -->
      <div>
        <button
          type="submit"
          :disabled="registerLoading"
          class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-black bg-white hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
        >
          <span v-if="registerLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
            <svg class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          {{ registerLoading ? 'กำลังสร้างบัญชี...' : 'สร้างบัญชี' }}
        </button>
      </div>
    </form>

    <!-- Switch Forms -->
    <div class="text-center mt-6">
      <button 
        v-if="!showRegister" 
        @click="showRegister = true"
        class="text-gray-400 hover:text-white text-sm"
      >
        ยังไม่มีบัญชี? สร้างบัญชีใหม่
      </button>
      <button 
        v-else 
        @click="showRegister = false"
        class="text-gray-400 hover:text-white text-sm"
      >
        มีบัญชีอยู่แล้ว? เข้าสู่ระบบ
      </button>
    </div>
  </div>
</template>

<script setup>
// Form data
const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

// UI state
const showRegister = ref(false)
const loginLoading = ref(false)
const registerLoading = ref(false)
const loginError = ref('')
const registerError = ref('')
const registerSuccess = ref('')

const { apiCall } = useApi()

// Login handler
const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    loginError.value = 'กรุณากรอกข้อมูลให้ครบถ้วน'
    return
  }

  loginLoading.value = true
  loginError.value = ''

  try {
    const response = await apiCall('/api/login', {
      method: 'POST',
      body: {
        username: loginForm.value.username,
        password: loginForm.value.password
      }
    })

    // บันทึก token และข้อมูลผู้ใช้
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))

    // Emit login success event
    emit('login-success', response.user)

    // ไปยังหน้าหลัก
    await navigateTo('/home')

  } catch (err) {
    console.error('Login error:', err)
    if (err.data?.error) {
      loginError.value = err.data.error
    } else {
      loginError.value = 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ'
    }
  } finally {
    loginLoading.value = false
  }
}

// Register handler
const handleRegister = async () => {
  registerError.value = ''
  registerSuccess.value = ''

  if (!validateForm()) {
    return
  }

  registerLoading.value = true

  try {
    const response = await apiCall('/api/register', {
      method: 'POST',
      body: {
        username: registerForm.value.username,
        password: registerForm.value.password
      }
    })

    registerSuccess.value = 'สร้างบัญชีสำเร็จ! กำลังไปยังหน้าเข้าสู่ระบบ...'
    
    // Emit register success event
    emit('register-success', response.user)
    
    // รีเซ็ตฟอร์ม
    registerForm.value = {
      username: '',
      password: '',
      confirmPassword: ''
    }

    // ไปยังหน้า login หลังจาก 2 วินาที
    setTimeout(async () => {
      showRegister.value = false
    }, 2000)

  } catch (err) {
    console.error('Register error:', err)
    if (err.data?.error) {
      registerError.value = err.data.error
    } else {
      registerError.value = 'เกิดข้อผิดพลาดในการสร้างบัญชี'
    }
  } finally {
    registerLoading.value = false
  }
}

// Form validation
const validateForm = () => {
  // ตรวจสอบความยาว username
  if (registerForm.value.username.length < 3) {
    registerError.value = 'ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร'
    return false
  }

  // ตรวจสอบความยาวรหัสผ่าน
  if (registerForm.value.password.length < 6) {
    registerError.value = 'รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร'
    return false
  }

  // ตรวจสอบการยืนยันรหัสผ่าน
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    registerError.value = 'รหัสผ่านไม่ตรงกัน'
    return false
  }

  return true
}

// Define emits
const emit = defineEmits(['login-success', 'register-success'])
</script>
