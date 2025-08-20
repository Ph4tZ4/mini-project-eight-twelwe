<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <div class="bg-gray-900 border-b border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <h1 class="text-3xl font-bold text-white">โปรไฟล์ผู้ใช้</h1>
          <button
            @click="goBack"
            class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md transition-colors duration-200"
          >
            กลับ
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Info -->
        <div class="lg:col-span-1">
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6">
            <div class="text-center">
              <!-- Profile Picture -->
              <div class="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden border-4 border-gray-700">
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
              </div>
              
              <!-- Username -->
              <h2 class="text-xl font-semibold text-white mb-2">
                {{ user?.username || 'กำลังโหลด...' }}
              </h2>
              
              <!-- Member Since -->
              <p class="text-gray-400 text-sm">
                สมาชิกตั้งแต่: {{ formatDate(user?.created_at) }}
              </p>
              
              <!-- Profile Picture Update Indicator -->
              <div v-if="profilePictureUpdated" class="mt-2">
                <p class="text-green-400 text-xs animate-pulse">
                  ✨ รูปโปรไฟล์อัปเดตแล้ว
                </p>
                <p class="text-gray-500 text-xs mt-1">
                  จาก {{ getUserInitials(usernameForm.newUsername) }} ({{ usernameForm.newUsername }})
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Forms -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Update Username Form -->
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-white mb-4">แก้ไขชื่อผู้ใช้</h3>
            
            <form @submit.prevent="updateUsername" class="space-y-4">
              <div>
                <label for="newUsername" class="block text-sm font-medium text-white mb-2">
                  ชื่อผู้ใช้ใหม่
                </label>
                <input
                  id="newUsername"
                  v-model="usernameForm.newUsername"
                  type="text"
                  required
                  minlength="3"
                  class="w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
                  placeholder="กรอกชื่อผู้ใช้ใหม่ (อย่างน้อย 3 ตัวอักษร)"
                />
                <p class="mt-1 text-xs text-gray-400">ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร</p>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium text-white mb-2">
                  รหัสผ่านปัจจุบัน
                </label>
                <input
                  id="password"
                  v-model="usernameForm.password"
                  type="password"
                  required
                  class="w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
                  placeholder="กรอกรหัสผ่านปัจจุบันเพื่อยืนยัน"
                />
              </div>

              <!-- Error/Success Messages -->
              <div v-if="usernameForm.error" class="text-red-400 text-sm bg-red-900 bg-opacity-20 p-3 rounded-md">
                {{ usernameForm.error }}
              </div>
              <div v-if="usernameForm.success" class="text-green-400 text-sm bg-green-900 bg-opacity-20 p-3 rounded-md">
                {{ usernameForm.success }}
              </div>

              <button
                type="submit"
                :disabled="usernameForm.loading"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="usernameForm.loading" class="flex items-center justify-center">
                  <svg class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  กำลังอัปเดต...
                </span>
                <span v-else>อัปเดตชื่อผู้ใช้</span>
              </button>
            </form>
          </div>

          <!-- Change Password Form -->
          <div class="bg-gray-900 rounded-lg border border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-white mb-4">เปลี่ยนรหัสผ่าน</h3>
            
            <form @submit.prevent="changePassword" class="space-y-4">
              <div>
                <label for="currentPassword" class="block text-sm font-medium text-white mb-2">
                  รหัสผ่านปัจจุบัน
                </label>
                <input
                  id="currentPassword"
                  v-model="passwordForm.currentPassword"
                  type="password"
                  required
                  class="w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
                  placeholder="กรอกรหัสผ่านปัจจุบัน"
                />
              </div>

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
                  class="w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
                  placeholder="กรอกรหัสผ่านใหม่ (อย่างน้อย 6 ตัวอักษร)"
                />
                <p class="mt-1 text-xs text-gray-400">รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร</p>
              </div>

              <div>
                <label for="confirmPassword" class="block text-sm font-medium text-white mb-2">
                  ยืนยันรหัสผ่านใหม่
                </label>
                <input
                  id="confirmPassword"
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  required
                  class="w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent"
                  placeholder="กรอกรหัสผ่านใหม่อีกครั้ง"
                />
              </div>

              <!-- Error/Success Messages -->
              <div v-if="passwordForm.error" class="text-red-400 text-sm bg-red-900 bg-opacity-20 p-3 rounded-md">
                {{ passwordForm.error }}
              </div>
              <div v-if="passwordForm.success" class="text-green-400 text-sm bg-green-900 bg-opacity-20 p-3 rounded-md">
                {{ passwordForm.success }}
              </div>

              <button
                type="submit"
                :disabled="passwordForm.loading"
                class="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
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
  password: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// User data
const user = ref(null)
const loading = ref(false)
const profilePictureUpdated = ref(false)

const { apiCall, isAuthenticated, getCurrentUser } = useApi()

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
    
    // Pre-fill username form
    usernameForm.value.newUsername = user.value.username
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
    }, 1000)
    
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
    const response = await apiCall('/api/profile/change-password', {
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

// Navigation
const goBack = () => {
  navigateTo('/home')
}

// Utility function to format date
const formatDate = (dateString) => {
  if (!dateString) return 'ไม่ทราบ'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('th-TH', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
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
</style>
