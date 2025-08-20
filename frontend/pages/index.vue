<template>
  <div class="min-h-screen bg-black text-white flex items-center justify-center">
    <!-- Loading State -->
    <div class="text-center">
      <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-6"></div>
      <h2 class="text-2xl font-bold text-white mb-2">กำลังโหลด...</h2>
      <p class="text-gray-400">กรุณารอสักครู่</p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'default'
})

// Check if user has visited before and redirect accordingly
onMounted(() => {
  const hasVisitedBefore = localStorage.getItem('hasVisitedBefore')
  
  if (!hasVisitedBefore) {
    // First time user - redirect to login page
    localStorage.setItem('hasVisitedBefore', 'true')
    navigateTo('/login')
  } else {
    // Returning user - check if they're already logged in
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    
    if (token && user) {
      // User is logged in - redirect to home page
      navigateTo('/home')
    } else {
      // User has visited before but not logged in - redirect to login
      navigateTo('/login')
    }
  }
})
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
