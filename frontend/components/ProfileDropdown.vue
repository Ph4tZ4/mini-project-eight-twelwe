<template>
  <div class="relative">
    <!-- Profile Picture Button -->
    <button
      @click="toggleDropdown"
      class="flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-black rounded-full"
    >
      <div class="w-10 h-10 rounded-full overflow-hidden border-2 border-white hover:border-gray-300 transition-colors">
        <img
          v-if="user?.profile_picture && isValidProfilePicture(user.profile_picture)"
          :src="user.profile_picture"
          :alt="user.username"
          class="w-full h-full object-cover"
          @error="handleImageError"
        />
        <div
          v-else
          class="w-full h-full bg-black flex items-center justify-center text-white font-bold text-lg"
        >
          {{ getUserInitials(user?.username) }}
        </div>
      </div>
      <svg
        class="w-4 h-4 text-white transition-transform duration-200"
        :class="{ 'rotate-180': isDropdownOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="isDropdownOpen"
      class="absolute right-0 mt-2 w-48 bg-gray-900 border border-gray-700 rounded-md shadow-lg z-50"
    >
      <!-- User Info -->
      <div class="px-4 py-3 border-b border-gray-700">
        <p class="text-sm text-white font-medium">{{ user?.username }}</p>
      </div>

      <!-- Menu Items -->
      <div class="py-1">
        <button
          @click="viewProfile"
          class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors flex items-center space-x-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span>ดูโปรไฟล์</span>
        </button>
        
        <!-- Admin Dashboard Link -->
        <button
          v-if="user?.is_admin"
          @click="goToAdminDashboard"
          class="w-full text-left px-4 py-2 text-sm text-yellow-300 hover:bg-gray-800 hover:text-yellow-200 transition-colors flex items-center space-x-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <span>ระบบผู้ดูแล</span>
        </button>
        
        <button
          @click="logout"
          class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors flex items-center space-x-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>ออกจากระบบ</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Props
const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

// Reactive state
const isDropdownOpen = ref(false)

// Debug logging
onMounted(() => {
  console.log('ProfileDropdown mounted with user:', props.user)
  if (props.user?.profile_picture) {
    console.log('Profile picture URL:', props.user.profile_picture)
    console.log('Profile picture starts with data:image:', props.user.profile_picture.startsWith('data:image'))
  }
})

// Methods
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}

const viewProfile = () => {
  closeDropdown()
  navigateTo('/profile')
}

const goToAdminDashboard = () => {
  closeDropdown()
  navigateTo('/admin/dashboard')
}

const logout = async () => {
  // Clear user data from localStorage
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  
  // Reset the visit flag so user goes to login page next time
  localStorage.removeItem('hasVisitedBefore')
  
  // Emit logout event
  emit('logout')
  
  // Close dropdown
  closeDropdown()
  
  // Redirect to login page
  await navigateTo('/login')
}

// Define emits
const emit = defineEmits(['logout'])

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

const isValidProfilePicture = (src) => {
  // Basic check for data URLs (e.g., "data:image/jpeg;base64,...")
  return src.startsWith('data:image/')
}

const handleImageError = (event) => {
  console.error('Profile picture failed to load:', event.target.src)
  // Fallback to default initials if image fails to load
  event.target.src = '' // Clear the src attribute to show the default
  event.target.alt = 'User' // Set a placeholder alt text
}

// Close dropdown when clicking outside
onMounted(() => {
  document.addEventListener('click', (event) => {
    const target = event.target
    if (!target.closest('.relative')) {
      closeDropdown()
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})
</script>
