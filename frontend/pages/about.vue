<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
          </div>
          
          <nav class="hidden md:flex space-x-8">
            <NuxtLink to="/" class="text-gray-300 hover:text-white transition-colors">หน้าแรก</NuxtLink>
            <NuxtLink to="/products" class="text-gray-300 hover:text-white transition-colors">สินค้า</NuxtLink>
            <NuxtLink to="/categories" class="text-gray-300 hover:text-white transition-colors">หมวดหมู่</NuxtLink>
            <NuxtLink to="/about" class="text-white font-semibold">เกี่ยวกับเรา</NuxtLink>
            <NuxtLink to="/contact" class="text-gray-300 hover:text-white transition-colors">ติดต่อ</NuxtLink>
          </nav>
          
          <div class="flex items-center space-x-4">
            <!-- Cart Icon -->
            <NuxtLink
              to="/cart"
              class="relative text-gray-300 hover:text-white transition-colors p-2"
              title="ตะกร้าสินค้า"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0H17"></path>
              </svg>
              <!-- Cart Count Badge -->
              <span 
                v-if="cartCount > 0" 
                class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
              >
                {{ cartCount > 99 ? '99+' : cartCount }}
              </span>
            </NuxtLink>
            
            <!-- Show ProfileDropdown when user is logged in -->
            <ProfileDropdown v-if="isLoggedIn" :user="currentUser" @logout="handleLogout" />
            
            <!-- Show Login/Register buttons when user is not logged in -->
            <template v-else>
              <NuxtLink
                to="/login"
                class="text-gray-300 hover:text-white transition-colors"
              >
                เข้าสู่ระบบ
              </NuxtLink>
              <NuxtLink
                to="/register"
                class="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors"
              >
                สมัครสมาชิก
              </NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main>
      <!-- Hero Section -->
      <section class="bg-black py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <!-- Loading state -->
          <div v-if="loading" class="py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-6"></div>
            <p class="text-gray-400">กำลังโหลดข้อมูล...</p>
          </div>
          
          <!-- Error state -->
          <div v-else-if="error" class="py-8">
            <p class="text-red-400 mb-4">{{ error }}</p>
            <button @click="fetchAboutData" class="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">
              ลองใหม่
            </button>
          </div>
          
          <!-- Content -->
          <div v-else>
            <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
              {{ aboutData.company_name || 'เกี่ยวกับเรา' }}
            </h1>
            <p class="text-xl text-gray-300 max-w-3xl mx-auto">
              {{ aboutData.tagline || 'ShopHub คือเว็บขายของออนไลน์ที่มุ่งมั่นให้บริการลูกค้าด้วยสินค้าคุณภาพสูง ราคาเป็นมิตร และบริการที่เหนือกว่า' }}
            </p>
          </div>
        </div>
      </section>

      <!-- Company Story -->
      <section class="py-20 bg-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 class="text-4xl font-bold text-white mb-6">เรื่องราวของเรา</h2>
              <p class="text-lg text-gray-300 mb-6">
                {{ aboutData.description || 'ShopHub เริ่มต้นจากการเป็นร้านค้าขนาดเล็กในปี 2020 ด้วยความมุ่งมั่นที่จะนำเสนอสินค้าคุณภาพสูง ให้กับลูกค้าทุกคนในราคาที่เป็นมิตร' }}
              </p>
              <p class="text-lg text-gray-300 mb-6">
                {{ aboutData.mission || 'ด้วยการพัฒนาอย่างต่อเนื่องและความไว้วางใจจากลูกค้า ShopHub ได้เติบโตขึ้นเป็นหนึ่งใน เว็บขายของออนไลน์ชั้นนำที่ลูกค้าไว้วางใจ' }}
              </p>
              <p class="text-lg text-gray-300">
                เราเชื่อว่าการให้บริการที่ดีที่สุดคือการเข้าใจความต้องการของลูกค้า และมุ่งมั่นที่จะ พัฒนาปรับปรุงบริการให้ดีขึ้นอย่างต่อเนื่อง
              </p>
            </div>
            <div class="bg-black border border-gray-800 rounded-lg p-8">
              <div class="text-center">
                <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg class="w-12 h-12 text-blue-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 class="text-2xl font-bold text-white mb-4">วิสัยทัศน์</h3>
                <p class="text-blue-100">
                  {{ aboutData.vision || 'เป็นผู้นำในธุรกิจอีคอมเมิร์ซที่ลูกค้าไว้วางใจและเลือกใช้บริการมากที่สุด' }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Mission & Values -->
      <section class="py-20 bg-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-white mb-4">พันธกิจและค่านิยม</h2>
            <p class="text-xl text-gray-300">สิ่งที่เราเชื่อและมุ่งมั่นที่จะทำ</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Mission -->
            <div class="bg-black border border-gray-800 p-8 rounded-lg text-center">
              <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
                <svg class="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-4">พันธกิจ</h3>
              <p class="text-gray-300">
                ให้บริการลูกค้าด้วยสินค้าคุณภาพสูง ราคาเป็นมิตร และบริการที่เหนือกว่า 
                เพื่อสร้างความพึงพอใจและความไว้วางใจสูงสุด
              </p>
            </div>
            
            <!-- Vision -->
            <div class="bg-black border border-gray-800 p-8 rounded-lg text-center">
              <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
                <svg class="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-4">วิสัยทัศน์</h3>
              <p class="text-gray-300">
                เป็นผู้นำในธุรกิจอีคอมเมิร์ซที่ลูกค้าไว้วางใจและเลือกใช้บริการมากที่สุด 
                ด้วยนวัตกรรมและเทคโนโลยีที่ทันสมัย
              </p>
            </div>
            
            <!-- Values -->
            <div class="bg-black border border-gray-800 p-8 rounded-lg text-center">
              <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
                <svg class="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-4">ค่านิยม</h3>
              <div class="text-gray-300 space-y-2">
                <div v-for="value in aboutData.values" :key="value" class="text-sm">
                  {{ value }}
                </div>
                <div v-if="aboutData.values.length === 0" class="text-sm">
                  ความซื่อสัตย์ ความรับผิดชอบ การพัฒนาอย่างต่อเนื่อง และการให้บริการที่ดีที่สุด เพื่อลูกค้าและสังคม
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Team Section -->
      <section class="py-20 bg-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-white mb-4">ทีมงานของเรา</h2>
            <p class="text-xl text-gray-300">ทีมงานที่มีความเชี่ยวชาญและมุ่งมั่นที่จะให้บริการที่ดีที่สุด</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Team Member -->
            <div v-for="member in aboutData.team" :key="member.name" class="bg-black p-6 rounded-lg text-center border border-gray-700">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl font-bold text-white">{{ member.name.charAt(0) }}</span>
              </div>
              <h3 class="text-xl font-semibold text-white mb-2">{{ member.name }}</h3>
              <p class="text-blue-400 mb-3">ทีมงาน</p>
              <p class="text-gray-400 text-sm">
                {{ member.description }}
              </p>
            </div>
            
            <!-- Fallback team members if no data -->
            <div v-if="aboutData.team.length === 0" class="bg-black p-6 rounded-lg text-center border border-gray-700">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl font-bold text-white">ก</span>
              </div>
              <h3 class="text-xl font-semibold text-white mb-2">คุณ กิตติศักดิ์ ใจดี</h3>
              <p class="text-blue-400 mb-3">CEO & Founder</p>
              <p class="text-gray-400 text-sm">
                ผู้นำที่มีวิสัยทัศน์และประสบการณ์มากกว่า 10 ปี ในธุรกิจอีคอมเมิร์ซ
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- History Section -->
      <section class="py-20 bg-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-white mb-4">ประวัติการพัฒนาของเรา</h2>
            <p class="text-xl text-gray-300">เส้นทางที่เราเดินมาพร้อมกับความสำเร็จ</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div v-for="milestone in aboutData.history" :key="milestone.year" class="bg-gray-900 p-6 rounded-lg text-center border border-gray-700">
              <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-xl font-bold text-black">{{ milestone.year }}</span>
              </div>
              <h3 class="text-lg font-semibold text-white mb-2">{{ milestone.title }}</h3>
              <p class="text-gray-300 text-sm">{{ milestone.description }}</p>
            </div>
            
            <!-- Fallback history if no data -->
            <div v-if="aboutData.history.length === 0" class="col-span-full text-center py-8">
              <p class="text-gray-400">ไม่มีข้อมูลประวัติ</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="py-20 bg-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div class="text-4xl font-bold text-white mb-2">10,000+</div>
              <p class="text-gray-300">ลูกค้าที่ไว้วางใจ</p>
            </div>
            <div>
              <div class="text-4xl font-bold text-white mb-2">50,000+</div>
              <p class="text-gray-300">สินค้าที่ขายได้</p>
            </div>
            <div>
              <div class="text-4xl font-bold text-white mb-2">99%</div>
              <p class="text-gray-300">ความพึงพอใจของลูกค้า</p>
            </div>
            <div>
              <div class="text-4xl font-bold text-white mb-2">24/7</div>
              <p class="text-gray-300">บริการลูกค้า</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-black border-t border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="text-center">
          <p class="text-gray-400">&copy; 2024 ShopHub. สงวนลิขสิทธิ์ทั้งหมด.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'default'
})

// Import the ProfileDropdown component
import ProfileDropdown from '~/components/ProfileDropdown.vue'

// Data for the about page
const aboutData = ref({
  company_name: '',
  tagline: '',
  description: '',
  mission: '',
  vision: '',
  values: [],
  history: [],
  team: [],
  contact_info: {}
})

// Authentication state
const isLoggedIn = ref(false)
const currentUser = ref(null)

const loading = ref(true)
const error = ref('')

const { apiCall } = useApi()
const { cartCount, getCartCount } = useCart()

// Check authentication status
const checkAuthStatus = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    try {
      currentUser.value = JSON.parse(user)
      isLoggedIn.value = true
    } catch (e) {
      console.error('Error parsing user data:', e)
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  } else {
    isLoggedIn.value = false
    currentUser.value = null
  }
}

// Handle logout event from ProfileDropdown
const handleLogout = () => {
  // Clear authentication state
  isLoggedIn.value = false
  currentUser.value = null
  
  // Clear localStorage
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('hasVisitedBefore')
  
  // Redirect to login page
  navigateTo('/login')
}

// Fetch about page data
const fetchAboutData = async () => {
  try {
    loading.value = true
    const response = await apiCall('/api/about', {
      method: 'GET'
    })
    
    if (response.success) {
      aboutData.value = response.about
    }
  } catch (err) {
    console.error('Error fetching about data:', err)
    error.value = 'เกิดข้อผิดพลาดในการดึงข้อมูล'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  checkAuthStatus()
  fetchAboutData()
  getCartCount() // Get cart count on mount
  
  // Listen for storage changes (login/logout)
  window.addEventListener('storage', checkAuthStatus)
})

onUnmounted(() => {
  window.removeEventListener('storage', checkAuthStatus)
})
</script>

<style scoped>
/* Custom scrollbar */
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
