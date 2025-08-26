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
            <NuxtLink to="/about" class="text-gray-300 hover:text-white transition-colors">เกี่ยวกับเรา</NuxtLink>
            <NuxtLink to="/contact" class="text-white font-semibold">ติดต่อ</NuxtLink>
          </nav>
          
          <div class="flex items-center space-x-4">
            <!-- Show ProfileDropdown if logged in, otherwise show Login/Register buttons -->
            <ProfileDropdown v-if="isLoggedIn" :user="currentUser" @logout="handleLogout" />
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
          <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
            ติดต่อเรา
          </h1>
          <p class="text-xl text-gray-300 max-w-3xl mx-auto">
            เรายินดีที่จะได้ยินจากคุณ หากมีคำถามหรือต้องการความช่วยเหลือ 
            กรุณาติดต่อเราได้เลย
          </p>
        </div>
      </section>

      <!-- Contact Form & Info -->
      <section class="py-20 bg-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <!-- Contact Form -->
            <div class="bg-black p-8 rounded-lg border border-gray-700">
              <h2 class="text-3xl font-bold text-white mb-6">ส่งข้อความถึงเรา</h2>
              
              <form @submit.prevent="submitContact" class="space-y-6">
                <!-- Name -->
                <div>
                  <label for="name" class="block text-sm font-medium text-white mb-2">
                    ชื่อ <span class="text-red-400">*</span>
                  </label>
                  <input
                    id="name"
                    v-model="form.name"
                    type="text"
                    required
                    class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white transition-colors"
                    placeholder="กรอกชื่อของคุณ"
                  />
                </div>

                <!-- Email -->
                <div>
                  <label for="email" class="block text-sm font-medium text-white mb-2">
                    อีเมล <span class="text-red-400">*</span>
                  </label>
                  <input
                    id="email"
                    v-model="form.email"
                    type="email"
                    required
                    class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white transition-colors"
                    placeholder="กรอกอีเมลของคุณ"
                  />
                </div>

                <!-- Phone -->
                <div>
                  <label for="phone" class="block text-sm font-medium text-white mb-2">
                    เบอร์โทรศัพท์
                  </label>
                  <input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white transition-colors"
                    placeholder="กรอกเบอร์โทรศัพท์ (ไม่บังคับ)"
                  />
                </div>

                <!-- Subject -->
                <div>
                  <label for="subject" class="block text-sm font-medium text-white mb-2">
                    หัวข้อ <span class="text-red-400">*</span>
                  </label>
                  <input
                    id="subject"
                    v-model="form.subject"
                    type="text"
                    required
                    class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white transition-colors"
                    placeholder="กรอกหัวข้อข้อความ"
                  />
                </div>

                <!-- Message -->
                <div>
                  <label for="message" class="block text-sm font-medium text-white mb-2">
                    ข้อความ <span class="text-red-400">*</span>
                  </label>
                  <textarea
                    id="message"
                    v-model="form.message"
                    rows="5"
                    required
                    class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-white transition-colors resize-none"
                    placeholder="กรอกข้อความของคุณ"
                  ></textarea>
                </div>

                <!-- Submit Button -->
                <button
                  type="submit"
                  :disabled="loading"
                  class="w-full bg-white text-black py-3 px-6 rounded-md font-semibold hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="loading" class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    กำลังส่งข้อความ...
                  </span>
                  <span v-else>ส่งข้อความ</span>
                </button>
              </form>

              <!-- Success/Error Messages -->
              <div v-if="success" class="mt-4 p-4 bg-green-900 bg-opacity-20 border border-green-700 rounded-md">
                <p class="text-green-400 text-center">{{ success }}</p>
              </div>

              <div v-if="error" class="mt-4 p-4 bg-red-900 bg-opacity-20 border border-red-700 rounded-md">
                <p class="text-red-400 text-center">{{ error }}</p>
              </div>
            </div>

            <!-- Contact Information -->
            <div class="space-y-8">
              <div>
                <h2 class="text-3xl font-bold text-white mb-6">ข้อมูลการติดต่อ</h2>
                <p class="text-gray-300 mb-8">
                  เราพร้อมให้บริการและตอบคำถามของคุณ ติดต่อเราได้หลายช่องทาง
                </p>
              </div>

              <!-- Contact Methods -->
              <div class="space-y-6">
                <!-- Phone -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white mb-1">โทรศัพท์</h3>
                    <p class="text-gray-300">02-123-4567</p>
                    <p class="text-gray-300">08-1234-5678</p>
                  </div>
                </div>

                <!-- Email -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white mb-1">อีเมล</h3>
                    <p class="text-gray-300">info@shophub.com</p>
                    <p class="text-gray-300">support@shophub.com</p>
                  </div>
                </div>

                <!-- Address -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white mb-1">ที่อยู่</h3>
                    <p class="text-gray-300">123 ถนนสุขุมวิท แขวงคลองเตย</p>
                    <p class="text-gray-300">เขตคลองเตย กรุงเทพมหานคร 10110</p>
                  </div>
                </div>

                <!-- Business Hours -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white mb-1">เวลาทำการ</h3>
                    <p class="text-gray-300">จันทร์ - ศุกร์: 9:00 - 18:00 น.</p>
                    <p class="text-gray-300">เสาร์ - อาทิตย์: 10:00 - 16:00 น.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ Section -->
      <section class="py-20 bg-black">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-white mb-4">คำถามที่พบบ่อย</h2>
            <p class="text-xl text-gray-300">คำตอบสำหรับคำถามที่ลูกค้าสงสัยมากที่สุด</p>
          </div>
          
          <div class="space-y-6">
            <div v-for="(faq, index) in faqs" :key="index" class="bg-gray-900 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-white mb-3">{{ faq.question }}</h3>
              <p class="text-gray-300">{{ faq.answer }}</p>
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

// Import ProfileDropdown component
import ProfileDropdown from '~/components/ProfileDropdown.vue'

const { apiCall } = useApi()

// Form data
const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const loading = ref(false)
const success = ref('')
const error = ref('')

// Authentication state
const isLoggedIn = ref(false)
const currentUser = ref(null)

// Check authentication status
const checkAuthStatus = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    isLoggedIn.value = true
    currentUser.value = JSON.parse(user)
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

// FAQ data
const faqs = ref([
  {
    question: 'วิธีการสั่งซื้อสินค้าทำอย่างไร?',
    answer: 'คุณสามารถเลือกสินค้าที่ต้องการ เพิ่มลงตะกร้า และทำการชำระเงินผ่านระบบออนไลน์ของเราได้เลย'
  },
  {
    question: 'มีบริการจัดส่งฟรีหรือไม่?',
    answer: 'เรามีบริการจัดส่งฟรีสำหรับออเดอร์ที่มีมูลค่าเกิน 1,000 บาท ทั่วประเทศ'
  },
  {
    question: 'สามารถคืนสินค้าได้หรือไม่?',
    answer: 'สามารถคืนสินค้าได้ภายใน 7-30 วัน ตามประเภทสินค้า โดยสินค้าต้องอยู่ในสภาพเดิม'
  },
  {
    question: 'ใช้เวลาจัดส่งนานเท่าไหร่?',
    answer: 'การจัดส่งภายในกรุงเทพฯ ใช้เวลา 1-2 วัน ส่วนต่างจังหวัดใช้เวลา 2-5 วัน'
  }
])

const submitContact = async () => {
  try {
    loading.value = true
    success.value = ''
    error.value = ''

    const response = await apiCall('/api/contact', {
      method: 'POST',
      body: form.value
    })

    if (response.success) {
      success.value = response.message
      // Reset form
      form.value = {
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      }
    }
  } catch (err) {
    console.error('Contact submission error:', err)
    if (err.data?.error) {
      error.value = err.data.error
    } else {
      error.value = 'เกิดข้อผิดพลาดในการส่งข้อความ กรุณาลองใหม่อีกครั้ง'
    }
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  checkAuthStatus() // Check authentication status on mount
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
