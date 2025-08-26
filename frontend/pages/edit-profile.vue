<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <div class="bg-gray-900 border-b border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center space-x-4">
            <button
              @click="goBack"
              class="bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-md transition-colors duration-200"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 class="text-3xl font-bold text-white">แก้ไขโปรไฟล์</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="viewProfile"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors duration-200"
            >
              ดูโปรไฟล์
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white"></div>
    </div>

    <!-- Main Content -->
    <div v-else class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Preview -->
        <div class="lg:col-span-1">
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6 sticky top-8">
            <h3 class="text-lg font-semibold text-white mb-4 text-center">ตัวอย่างโปรไฟล์</h3>
            <div class="text-center">
              <!-- Profile Picture -->
              <div class="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden border-4 border-gray-700 relative">
                <img
                  v-if="user?.profile_picture"
                  :src="user.profile_picture"
                  :alt="user?.username"
                  class="w-full h-full object-cover transition-all duration-300"
                  :class="{ 'scale-110': profilePictureUpdated }"
                />
                <div
                  v-else
                  class="w-full h-full bg-gray-700 flex items-center justify-center text-4xl font-bold text-white"
                >
                  {{ getUserInitials(user?.username) }}
                </div>
                
                <!-- Update indicator -->
                <div 
                  v-if="profilePictureUpdated" 
                  class="absolute inset-0 bg-green-500 bg-opacity-20 flex items-center justify-center rounded-full"
                >
                  <div class="bg-green-500 rounded-full p-2">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <!-- Username -->
              <h2 class="text-xl font-semibold text-white mb-2">
                {{ user?.username || 'กำลังโหลด...' }}
              </h2>
              
              <!-- Member Since -->
              <p class="text-gray-400 text-sm">
                สมาชิกตั้งแต่: {{ formatDate(user?.created_at) }}
              </p>
              
              <!-- Last Updated -->
              <p class="text-gray-500 text-xs mt-2">
                อัปเดตล่าสุด: {{ formatDate(user?.updated_at) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Edit Forms -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Personal Information Section -->
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-white flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                ข้อมูลส่วนตัว
              </h3>
              <div class="text-xs text-gray-400 bg-gray-800 px-3 py-1 rounded-full">
                กรอกรหัสผ่านเพื่อยืนยันการเปลี่ยนแปลง
              </div>
            </div>
            
            <form @submit.prevent="updateUsername" class="space-y-6">
              <div class="grid grid-cols-1 gap-6">
                <!-- Username Field -->
                <div>
                  <label for="newUsername" class="block text-sm font-medium text-white mb-2">
                    ชื่อผู้ใช้
                  </label>
                  <div class="relative">
                    <input
                      id="newUsername"
                      v-model="usernameForm.newUsername"
                      type="text"
                      required
                      minlength="3"
                      class="w-full px-4 py-3 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                      placeholder="กรอกชื่อผู้ใช้ใหม่"
                      :class="{ 'border-red-500': usernameForm.error, 'border-green-500': usernameForm.success }"
                    />
                    <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <svg v-if="usernameForm.success" class="h-5 w-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                  <p class="mt-1 text-xs text-gray-400">ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร และไม่ซ้ำกับผู้อื่น</p>
                </div>

                <!-- Current Password for Verification -->
                <div>
                  <label for="verifyPassword" class="block text-sm font-medium text-white mb-2">
                    รหัสผ่านปัจจุบัน
                  </label>
                  <input
                    id="verifyPassword"
                    v-model="usernameForm.password"
                    type="password"
                    required
                    class="w-full px-4 py-3 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    placeholder="กรอกรหัสผ่านปัจจุบันเพื่อยืนยัน"
                  />
                </div>
              </div>

              <!-- Error/Success Messages -->
              <div v-if="usernameForm.error" class="text-red-400 text-sm bg-red-900 bg-opacity-20 p-4 rounded-md border border-red-800">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ usernameForm.error }}
                </div>
              </div>
              <div v-if="usernameForm.success" class="text-green-400 text-sm bg-green-900 bg-opacity-20 p-4 rounded-md border border-green-800">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  {{ usernameForm.success }}
                </div>
              </div>

              <button
                type="submit"
                :disabled="usernameForm.loading || !hasUsernameChanged"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                <span v-if="usernameForm.loading" class="flex items-center justify-center">
                  <svg class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  กำลังอัปเดต...
                </span>
                <span v-else>{{ hasUsernameChanged ? 'บันทึกการเปลี่ยนแปลง' : 'ไม่มีการเปลี่ยนแปลง' }}</span>
              </button>
            </form>
          </div>

          <!-- Security Section -->
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-white flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                ความปลอดภัย
              </h3>
              <div class="text-xs text-gray-400 bg-gray-800 px-3 py-1 rounded-full">
                เปลี่ยนรหัสผ่านเพื่อความปลอดภัย
              </div>
            </div>
            
            <form @submit.prevent="changePassword" class="space-y-6">
              <div class="grid grid-cols-1 gap-6">
                <!-- Current Password -->
                <div>
                  <label for="currentPassword" class="block text-sm font-medium text-white mb-2">
                    รหัสผ่านปัจจุบัน
                  </label>
                  <input
                    id="currentPassword"
                    v-model="passwordForm.currentPassword"
                    type="password"
                    required
                    class="w-full px-4 py-3 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                    placeholder="กรอกรหัสผ่านปัจจุบัน"
                  />
                </div>

                <!-- New Password -->
                <div>
                  <label for="newPassword" class="block text-sm font-medium text-white mb-2">
                    รหัสผ่านใหม่
                  </label>
                  <input
                    id="newPassword"
                    v-model="passwordForm.newPassword"
                    type="password"
                    required
                    minlength="6"
                    class="w-full px-4 py-3 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                    placeholder="กรอกรหัสผ่านใหม่"
                    :class="{ 'border-red-500': passwordMismatch, 'border-green-500': passwordMatch && passwordForm.newPassword.length >= 6 }"
                  />
                  <div class="mt-2">
                    <div class="text-xs text-gray-400 mb-1">ความแข็งแกร่งของรหัสผ่าน:</div>
                    <div class="flex space-x-1">
                      <div v-for="i in 4" :key="i" class="flex-1 h-1 rounded" :class="getPasswordStrengthColor(i)"></div>
                    </div>
                    <div class="text-xs mt-1" :class="getPasswordStrengthTextColor()">
                      {{ getPasswordStrengthText() }}
                    </div>
                  </div>
                </div>

                <!-- Confirm Password -->
                <div>
                  <label for="confirmPassword" class="block text-sm font-medium text-white mb-2">
                    ยืนยันรหัสผ่านใหม่
                  </label>
                  <input
                    id="confirmPassword"
                    v-model="passwordForm.confirmPassword"
                    type="password"
                    required
                    class="w-full px-4 py-3 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                    placeholder="กรอกรหัสผ่านใหม่อีกครั้ง"
                    :class="{ 'border-red-500': passwordMismatch, 'border-green-500': passwordMatch }"
                  />
                  <p v-if="passwordMismatch && passwordForm.confirmPassword" class="mt-1 text-xs text-red-400">
                    รหัสผ่านไม่ตรงกัน
                  </p>
                  <p v-if="passwordMatch && passwordForm.confirmPassword" class="mt-1 text-xs text-green-400">
                    รหัสผ่านตรงกัน
                  </p>
                </div>
              </div>

              <!-- Error/Success Messages -->
              <div v-if="passwordForm.error" class="text-red-400 text-sm bg-red-900 bg-opacity-20 p-4 rounded-md border border-red-800">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ passwordForm.error }}
                </div>
              </div>
              <div v-if="passwordForm.success" class="text-green-400 text-sm bg-green-900 bg-opacity-20 p-4 rounded-md border border-green-800">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  {{ passwordForm.success }}
                </div>
              </div>

              <button
                type="submit"
                :disabled="passwordForm.loading || !passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword || passwordMismatch"
                class="w-full bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                <span v-if="passwordForm.loading" class="flex items-center justify-center">
                  <svg class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  กำลังเปลี่ยนรหัสผ่าน...
                </span>
                <span v-else>เปลี่ยนรหัสผ่าน</span>
              </button>
            </form>
          </div>

          <!-- Account Information Section -->
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              ข้อมูลบัญชี
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-gray-800 p-4 rounded-md">
                <div class="text-sm text-gray-400 mb-1">รหัสผู้ใช้</div>
                <div class="text-white font-mono text-sm">{{ user?.id || 'กำลังโหลด...' }}</div>
              </div>
              
              <div class="bg-gray-800 p-4 rounded-md">
                <div class="text-sm text-gray-400 mb-1">วันที่สร้างบัญชี</div>
                <div class="text-white text-sm">{{ formatDate(user?.created_at) }}</div>
              </div>
              
              <div class="bg-gray-800 p-4 rounded-md">
                <div class="text-sm text-gray-400 mb-1">อัปเดตล่าสุด</div>
                <div class="text-white text-sm">{{ formatDate(user?.updated_at) }}</div>
              </div>
              
              <div class="bg-gray-800 p-4 rounded-md">
                <div class="text-sm text-gray-400 mb-1">รูปโปรไฟล์</div>
                <div class="text-white text-sm">สร้างอัตโนมัติจากชื่อผู้ใช้</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'default'
})

// Form data
const usernameForm = ref({
  newUsername: '',
  password: '',
  loading: false,
  error: '',
  success: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
  loading: false,
  error: '',
  success: ''
})

// User data
const user = ref(null)
const loading = ref(false)
const profilePictureUpdated = ref(false)
const originalUsername = ref('')

const { apiCall, isAuthenticated, getCurrentUser } = useApi()

// Computed properties
const hasUsernameChanged = computed(() => {
  return usernameForm.value.newUsername !== originalUsername.value
})

const passwordMatch = computed(() => {
  return passwordForm.value.newPassword === passwordForm.value.confirmPassword && 
         passwordForm.value.newPassword.length > 0
})

const passwordMismatch = computed(() => {
  return passwordForm.value.newPassword !== passwordForm.value.confirmPassword && 
         passwordForm.value.confirmPassword.length > 0
})

// Check authentication and load user data
onMounted(async () => {
  if (!isAuthenticated()) {
    await navigateTo('/login')
    return
  }

  await loadUserProfile()
})

// Load user profile
const loadUserProfile = async () => {
  try {
    loading.value = true
    const response = await apiCall('/api/profile')
    user.value = response.user
    
    // Pre-fill username form and store original
    usernameForm.value.newUsername = user.value.username
    originalUsername.value = user.value.username
  } catch (error) {
    console.error('Error loading profile:', error)
    if (error.status === 401) {
      await navigateTo('/login')
    }
  } finally {
    loading.value = false
  }
}

// Update username
const updateUsername = async () => {
  if (!usernameForm.value.newUsername || !usernameForm.value.password) {
    usernameForm.value.error = 'กรุณากรอกข้อมูลให้ครบถ้วน'
    return
  }

  if (usernameForm.value.newUsername.length < 3) {
    usernameForm.value.error = 'ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร'
    return
  }

  if (!hasUsernameChanged.value) {
    usernameForm.value.error = 'ไม่มีการเปลี่ยนแปลงชื่อผู้ใช้'
    return
  }

  usernameForm.value.loading = true
  usernameForm.value.error = ''
  usernameForm.value.success = ''

  try {
    const response = await apiCall('/api/profile/update', {
      method: 'PUT',
      body: {
        username: usernameForm.value.newUsername,
        password: usernameForm.value.password
      }
    })

    usernameForm.value.success = 'อัปเดตชื่อผู้ใช้และรูปโปรไฟล์สำเร็จ!'
    
    // Update local user data including profile picture
    user.value.username = usernameForm.value.newUsername
    user.value.profile_picture = response.user.profile_picture
    originalUsername.value = usernameForm.value.newUsername
    
    // Update localStorage
    const currentUser = getCurrentUser()
    if (currentUser) {
      currentUser.username = usernameForm.value.newUsername
      currentUser.profile_picture = response.user.profile_picture
      localStorage.setItem('user', JSON.stringify(currentUser))
    }
    
    // Trigger profile picture update animation
    profilePictureUpdated.value = true
    setTimeout(() => {
      profilePictureUpdated.value = false
    }, 2000)
    
    // Clear password field
    usernameForm.value.password = ''
    
  } catch (error) {
    console.error('Error updating username:', error)
    if (error.data?.error) {
      usernameForm.value.error = error.data.error
    } else {
      usernameForm.value.error = 'เกิดข้อผิดพลาดในการอัปเดตชื่อผู้ใช้'
    }
  } finally {
    usernameForm.value.loading = false
  }
}

// Change password
const changePassword = async () => {
  if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
    passwordForm.value.error = 'กรุณากรอกข้อมูลให้ครบถ้วน'
    return
  }

  if (passwordForm.value.newPassword.length < 6) {
    passwordForm.value.error = 'รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร'
    return
  }

  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordForm.value.error = 'รหัสผ่านใหม่ไม่ตรงกัน'
    return
  }

  passwordForm.value.loading = true
  passwordForm.value.error = ''
  passwordForm.value.success = ''

  try {
    await apiCall('/api/profile/change-password', {
      method: 'PUT',
      body: {
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword
      }
    })

    passwordForm.value.success = 'เปลี่ยนรหัสผ่านสำเร็จ!'
    
    // Clear form
    passwordForm.value.currentPassword = ''
    passwordForm.value.newPassword = ''
    passwordForm.value.confirmPassword = ''
    
  } catch (error) {
    console.error('Error changing password:', error)
    if (error.data?.error) {
      passwordForm.value.error = error.data.error
    } else {
      passwordForm.value.error = 'เกิดข้อผิดพลาดในการเปลี่ยนรหัสผ่าน'
    }
  } finally {
    passwordForm.value.loading = false
  }
}

// Password strength calculation
const getPasswordStrength = () => {
  const password = passwordForm.value.newPassword
  if (!password) return 0
  
  let strength = 0
  if (password.length >= 6) strength++
  if (password.length >= 8) strength++
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) strength++
  if (/\d/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  
  return Math.min(strength, 4)
}

const getPasswordStrengthColor = (index) => {
  const strength = getPasswordStrength()
  if (index <= strength) {
    if (strength <= 1) return 'bg-red-500'
    if (strength <= 2) return 'bg-yellow-500'
    if (strength <= 3) return 'bg-blue-500'
    return 'bg-green-500'
  }
  return 'bg-gray-600'
}

const getPasswordStrengthText = () => {
  const strength = getPasswordStrength()
  const texts = ['อ่อนแอมาก', 'อ่อนแอ', 'ปานกลาง', 'แข็งแกร่ง', 'แข็งแกร่งมาก']
  return texts[strength] || 'ไม่มีรหัสผ่าน'
}

const getPasswordStrengthTextColor = () => {
  const strength = getPasswordStrength()
  if (strength <= 1) return 'text-red-400'
  if (strength <= 2) return 'text-yellow-400'
  if (strength <= 3) return 'text-blue-400'
  return 'text-green-400'
}

// Navigation
const goBack = () => {
  navigateTo('/profile')
}

const viewProfile = () => {
  navigateTo('/profile')
}

// Utility function to format date
const formatDate = (dateString) => {
  if (!dateString) return 'ไม่ทราบ'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('th-TH', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return 'ไม่ทราบ'
  }
}

// Utility function to get user initials (same logic as backend)
const getUserInitials = (username) => {
  if (!username) return 'U'
  
  // Use the exact same logic as backend for consistency
  const words = username.match(/[A-Z][a-z]*|[a-z]+/g)
  
  if (!words) {
    return username[0]?.toUpperCase() || 'U'
  }
  
  // Get initials from first letters of each word (max 2)
  const initials = words.slice(0, 2).map(word => word[0].toUpperCase()).join('')
  return initials || username[0]?.toUpperCase() || 'U'
}

// Clear success/error messages when user starts typing
watch(() => usernameForm.value.newUsername, () => {
  if (usernameForm.value.success) {
    usernameForm.value.success = ''
  }
  if (usernameForm.value.error) {
    usernameForm.value.error = ''
  }
})

watch(() => [passwordForm.value.currentPassword, passwordForm.value.newPassword, passwordForm.value.confirmPassword], () => {
  if (passwordForm.value.success) {
    passwordForm.value.success = ''
  }
  if (passwordForm.value.error) {
    passwordForm.value.error = ''
  }
}, { deep: true })
</script>

<style scoped>
/* Custom scrollbar for webkit browsers */
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

/* Smooth transitions for form elements */
input:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Animation for profile picture update */
@keyframes profileUpdate {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.profile-update {
  animation: profileUpdate 0.6s ease-in-out;
}
</style>
