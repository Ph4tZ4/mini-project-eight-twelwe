<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Header -->
    <header class="bg-black border-b border-gray-800 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
        <div class="flex items-center gap-4">
          <NuxtLink to="/cart" class="text-gray-300 hover:text-white transition-colors">
            กลับไปตะกร้า
          </NuxtLink>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Progress Steps -->
      <div class="mb-8">
        <div class="flex items-center justify-center space-x-4">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="ml-2 text-sm text-gray-400">ตะกร้าสินค้า</span>
          </div>
          <div class="w-8 h-0.5 bg-gray-600"></div>
          <div class="flex items-center">
            <div class="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center">
              <span class="text-sm font-semibold">2</span>
            </div>
            <span class="ml-2 text-sm text-white font-semibold">ชำระเงิน</span>
          </div>
          <div class="w-8 h-0.5 bg-gray-600"></div>
          <div class="flex items-center">
            <div class="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
              <span class="text-sm">3</span>
            </div>
            <span class="ml-2 text-sm text-gray-400">ยืนยันคำสั่งซื้อ</span>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-400">กำลังโหลด...</p>
      </div>

      <!-- Main Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Checkout Form -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Shipping Address -->
          <div class="bg-gray-900 rounded-lg p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                ที่อยู่สำหรับจัดส่ง
              </h2>
              
              <button
                @click="useCurrentLocation"
                :disabled="gettingLocation"
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 text-sm"
              >
                <svg v-if="gettingLocation" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                {{ gettingLocation ? 'กำลังค้นหา...' : 'ใช้ที่อยู่ปัจจุบัน' }}
              </button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">ชื่อ-นามสกุล</label>
                <input
                  v-model="shippingForm.full_name"
                  type="text"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  placeholder="กรุณากรอกชื่อ-นามสกุล"
                  required
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">เบอร์โทรศัพท์</label>
                <input
                  v-model="shippingForm.phone"
                  type="tel"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  placeholder="กรุณากรอกเบอร์โทรศัพท์"
                  required
                />
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-300 mb-2">ที่อยู่</label>
                <input
                  v-model="shippingForm.address_line_1"
                  type="text"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  placeholder="เลขที่ ซอย ถนน"
                  required
                />
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-300 mb-2">ที่อยู่เพิ่มเติม (ไม่บังคับ)</label>
                <input
                  v-model="shippingForm.address_line_2"
                  type="text"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  placeholder="ตึก อาคาร คอนโด"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">จังหวัด</label>
                <select
                  v-model="shippingForm.province"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  required
                >
                  <option value="">เลือกจังหวัด</option>
                  <option v-for="province in provinces" :key="province" :value="province">
                    {{ province }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">เมือง/อำเภอ</label>
                <input
                  v-model="shippingForm.city"
                  type="text"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  placeholder="เมือง/อำเภอ"
                  required
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">รหัสไปรษณีย์</label>
                <input
                  v-model="shippingForm.postal_code"
                  type="text"
                  maxlength="5"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
                  placeholder="รหัสไปรษณีย์"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Payment Method -->
          <div class="bg-gray-900 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
              </svg>
              วิธีการชำระเงิน
            </h2>
            
            <div class="space-y-3">
              <label class="flex items-center p-4 border border-gray-700 rounded-lg cursor-pointer hover:border-gray-600 transition-colors">
                <input
                  v-model="paymentMethod"
                  type="radio"
                  value="cash_on_delivery"
                  class="w-4 h-4 text-white border-gray-600 focus:ring-white"
                />
                <div class="ml-3 flex-1">
                  <div class="flex items-center gap-3">
                    <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                    </svg>
                    <div>
                      <p class="font-medium">เก็บเงินปลายทาง (Cash on Delivery)</p>
                      <p class="text-sm text-gray-400">ชำระเงินเมื่อได้รับสินค้า</p>
                    </div>
                  </div>
                </div>
              </label>
              
              <label class="flex items-center p-4 border border-gray-700 rounded-lg cursor-pointer hover:border-gray-600 transition-colors opacity-50">
                <input
                  type="radio"
                  value="credit_card"
                  disabled
                  class="w-4 h-4 text-white border-gray-600 focus:ring-white"
                />
                <div class="ml-3 flex-1">
                  <div class="flex items-center gap-3">
                    <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
                    </svg>
                    <div>
                      <p class="font-medium">บัตรเครดิต/เดบิต</p>
                      <p class="text-sm text-gray-400">เร็วๆ นี้ (ยังไม่พร้อมใช้งาน)</p>
                    </div>
                  </div>
                </div>
              </label>
              
              <label class="flex items-center p-4 border border-gray-700 rounded-lg cursor-pointer hover:border-gray-600 transition-colors opacity-50">
                <input
                  type="radio"
                  value="bank_transfer"
                  disabled
                  class="w-4 h-4 text-white border-gray-600 focus:ring-white"
                />
                <div class="ml-3 flex-1">
                  <div class="flex items-center gap-3">
                    <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path>
                    </svg>
                    <div>
                      <p class="font-medium">โอนเงินผ่านธนาคาร</p>
                      <p class="text-sm text-gray-400">เร็วๆ นี้ (ยังไม่พร้อมใช้งาน)</p>
                    </div>
                  </div>
                </div>
              </label>
            </div>
          </div>

          <!-- Order Notes -->
          <div class="bg-gray-900 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4">หมายเหตุสำหรับคำสั่งซื้อ (ไม่บังคับ)</h2>
            <textarea
              v-model="orderNotes"
              rows="3"
              class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 focus:border-white focus:outline-none"
              placeholder="ข้อความเพิ่มเติมสำหรับผู้ขาย..."
            ></textarea>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="bg-gray-900 rounded-lg p-6 h-fit sticky top-24">
          <h2 class="text-xl font-semibold mb-6 border-b border-gray-800 pb-3">สรุปคำสั่งซื้อ</h2>
          
          <!-- Cart Items -->
          <div class="space-y-3 mb-6">
            <div v-for="item in cartItems" :key="item.product.id" class="flex justify-between items-center">
              <div class="flex-1">
                <p class="text-sm font-medium">{{ item.product.name }}</p>
                <p class="text-xs text-gray-400">{{ item.quantity }} x ฿{{ formatPrice(item.price_at_add) }}</p>
              </div>
              <p class="text-sm font-semibold">฿{{ formatPrice(item.price_at_add * item.quantity) }}</p>
            </div>
          </div>
          
          <hr class="border-gray-700 mb-4">
          
          <!-- Pricing -->
          <div class="space-y-2 mb-6">
            <div class="flex justify-between text-gray-300">
              <span>ยอดรวมสินค้า</span>
              <span>฿{{ formatPrice(cartTotals.subtotal) }}</span>
            </div>
            <div class="flex justify-between text-gray-300">
              <span>ค่าจัดส่ง</span>
              <span>{{ cartTotals.subtotal >= 1000 ? 'ฟรี' : '฿50' }}</span>
            </div>
            <div class="flex justify-between text-gray-300">
              <span>ภาษี (7%)</span>
              <span>฿{{ formatPrice(calculateTax()) }}</span>
            </div>
            <hr class="border-gray-700">
            <div class="flex justify-between text-white text-lg font-semibold">
              <span>ยอดรวมทั้งหมด</span>
              <span>฿{{ formatPrice(calculateTotal()) }}</span>
            </div>
          </div>

          <!-- Place Order Button -->
          <button 
            @click="placeOrder"
            :disabled="!canPlaceOrder || placing"
            class="w-full bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ placing ? 'กำลังสั่งซื้อ...' : 'สั่งซื้อสินค้า' }}
          </button>
          
          <p class="text-xs text-gray-400 mt-3 text-center">
            การกดสั่งซื้อหมายความว่าคุณยอมรับ
            <a href="#" class="text-white underline">เงื่อนไขการใช้งาน</a>
          </p>
        </div>
      </div>
    </main>

    <!-- Notification -->
    <div 
      v-if="notification.show" 
      class="fixed bottom-4 right-4 z-50 transition-all duration-300"
      :class="notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'"
    >
      <div class="px-6 py-4 rounded-lg text-white max-w-sm">
        <div class="flex items-center gap-2">
          <svg v-if="notification.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          <span>{{ notification.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ 
  layout: 'default',
  middleware: 'auth'
})

const { apiCall } = useApi()
const { items: cartItems, totals: cartTotals, fetchCart } = useCart()

// Loading states
const loading = ref(true)
const placing = ref(false)
const gettingLocation = ref(false)

// Form data
const shippingForm = ref({
  full_name: '',
  phone: '',
  address_line_1: '',
  address_line_2: '',
  city: '',
  province: '',
  postal_code: '',
  country: 'Thailand'
})

// Auto-fill user name on load
const fillUserName = async () => {
  try {
    const response = await apiCall('/api/profile')
    if (response.user) {
      const { first_name, last_name } = response.user
      if (first_name || last_name) {
        shippingForm.value.full_name = `${first_name} ${last_name}`.trim()
      } else {
        // Fallback to username if no first/last name
        shippingForm.value.full_name = response.user.username || ''
      }
    }
  } catch (error) {
    console.error('Error fetching user profile:', error)
    // Fallback: try to get username from stored user data
    try {
      const userData = localStorage.getItem('user')
      if (userData) {
        const user = JSON.parse(userData)
        const { first_name, last_name, username } = user
        if (first_name || last_name) {
          shippingForm.value.full_name = `${first_name || ''} ${last_name || ''}`.trim()
        } else {
          shippingForm.value.full_name = username || ''
        }
      }
    } catch (fallbackError) {
      console.error('Error with fallback user data:', fallbackError)
    }
  }
}

const paymentMethod = ref('cash_on_delivery')
const orderNotes = ref('')
const provinces = ref([])

// Notification system
const notification = ref({ show: false, message: '', type: 'success' })

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 5000)
}

// Computed properties
const canPlaceOrder = computed(() => {
  return shippingForm.value.full_name &&
         shippingForm.value.phone &&
         shippingForm.value.address_line_1 &&
         shippingForm.value.city &&
         shippingForm.value.province &&
         shippingForm.value.postal_code &&
         paymentMethod.value &&
         cartItems.value.length > 0
})

// Calculations
const formatPrice = (price) => Number(price || 0).toLocaleString('th-TH')

const calculateShipping = () => {
  return cartTotals.value.subtotal >= 1000 ? 0 : 50
}

const calculateTax = () => {
  return cartTotals.value.subtotal * 0.07
}

const calculateTotal = () => {
  return cartTotals.value.subtotal + calculateShipping() + calculateTax()
}

// Methods
const fetchProvinces = async () => {
  try {
    const response = await apiCall('/api/provinces')
    if (response.success) {
      provinces.value = response.provinces
    }
  } catch (error) {
    console.error('Error fetching provinces:', error)
  }
}

const useCurrentLocation = async () => {
  gettingLocation.value = true
  
  try {
    // Check if geolocation is supported
    if (!navigator.geolocation) {
      showNotification('เบราว์เซอร์ของคุณไม่รองรับการระบุตำแหน่ง', 'error')
      return
    }

    // Get user's current position
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        resolve,
        reject,
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000
        }
      )
    })

    const { latitude, longitude } = position.coords

    // Use a free geocoding service (OpenStreetMap Nominatim)
    const geocodeResponse = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&accept-language=th,en`
    )
    
    if (!geocodeResponse.ok) {
      throw new Error('ไม่สามารถระบุที่อยู่ได้')
    }

    const geocodeData = await geocodeResponse.json()
    
    if (geocodeData && geocodeData.display_name) {
      // Parse the address components
      const address = geocodeData.address || {}
      
      // Map the address components to our form
      const addressMapping = {
        road: address.road || '',
        house_number: address.house_number || '',
        suburb: address.suburb || address.neighbourhood || address.quarter || '',
        city: address.city || address.town || address.municipality || address.village || '',
        province: address.state || address.province || '',
        postcode: address.postcode || '',
        country: address.country || 'Thailand'
      }

      // Build address line 1
      let addressLine1 = ''
      if (addressMapping.house_number) {
        addressLine1 += addressMapping.house_number + ' '
      }
      if (addressMapping.road) {
        addressLine1 += addressMapping.road
      }
      if (!addressLine1.trim()) {
        addressLine1 = addressMapping.suburb || 'ที่อยู่ปัจจุบัน'
      }

      // Add coordinates to address line 1
      const coordinates = `(${latitude.toFixed(6)}, ${longitude.toFixed(6)})`
      addressLine1 = `${addressLine1.trim()} ${coordinates}`

      // Update the form with detected location
      shippingForm.value.address_line_1 = addressLine1
      shippingForm.value.address_line_2 = addressMapping.suburb && addressMapping.suburb !== addressLine1 ? addressMapping.suburb : ''
      shippingForm.value.city = addressMapping.city
      
      // Try to match province with our list
      if (addressMapping.province) {
        const matchedProvince = provinces.value.find(p => 
          p.includes(addressMapping.province) || addressMapping.province.includes(p)
        )
        if (matchedProvince) {
          shippingForm.value.province = matchedProvince
        } else {
          shippingForm.value.province = addressMapping.province
        }
      }
      
      shippingForm.value.postal_code = addressMapping.postcode
      shippingForm.value.country = addressMapping.country

      showNotification('ระบุที่อยู่ปัจจุบันเรียบร้อยแล้ว', 'success')
    } else {
      throw new Error('ไม่สามารถระบุที่อยู่ได้')
    }

  } catch (error) {
    console.error('Geolocation error:', error)
    
    if (error.code === 1) {
      showNotification('กรุณาอนุญาตให้เข้าถึงตำแหน่งของคุณ', 'error')
    } else if (error.code === 2) {
      showNotification('ไม่สามารถระบุตำแหน่งได้', 'error')
    } else if (error.code === 3) {
      showNotification('หมดเวลาในการระบุตำแหน่ง', 'error')
    } else {
      showNotification('เกิดข้อผิดพลาดในการระบุตำแหน่ง กรุณากรอกที่อยู่ด้วยตนเอง', 'error')
    }
  } finally {
    gettingLocation.value = false
  }
}

const placeOrder = async () => {
  if (!canPlaceOrder.value) {
    showNotification('กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
    return
  }

  placing.value = true
  
  try {
    const orderData = {
      shipping_address: shippingForm.value,
      payment_method: paymentMethod.value,
      notes: orderNotes.value
    }

    const response = await apiCall('/api/checkout', {
      method: 'POST',
      body: orderData
    })

    if (response.success) {
      showNotification('สั่งซื้อสินค้าเรียบร้อยแล้ว!', 'success')
      // Redirect to order confirmation page
      setTimeout(() => {
        navigateTo(`/order-confirmation/${response.order.order_number}`)
      }, 2000)
    } else {
      showNotification(response.message || 'เกิดข้อผิดพลาดในการสั่งซื้อ', 'error')
    }
  } catch (error) {
    console.error('Error placing order:', error)
    showNotification('เกิดข้อผิดพลาดในการสั่งซื้อ', 'error')
  } finally {
    placing.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    fetchCart(),
    fetchProvinces()
  ])
  
  // Auto-fill user name
  await fillUserName()
  
  // Redirect if cart is empty
  if (!cartItems.value || cartItems.value.length === 0) {
    showNotification('ตะกร้าสินค้าว่างเปล่า กรุณาเลือกสินค้าก่อน', 'error')
    setTimeout(() => {
      navigateTo('/products')
    }, 2000)
    return
  }
  
  loading.value = false
})
</script>
