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
            <NuxtLink to="/contact" class="text-gray-300 hover:text-white transition-colors">ติดต่อ</NuxtLink>
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

    <!-- Loading State -->
    <div v-if="loading" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        <p class="mt-4 text-gray-300">กำลังโหลดข้อมูลสินค้า...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="text-center py-20">
        <div class="text-red-500 text-6xl mb-4">⚠️</div>
        <h1 class="text-2xl font-bold text-white mb-4">ไม่พบสินค้า</h1>
        <p class="text-gray-300 mb-8">{{ error }}</p>
        <NuxtLink
          to="/products"
          class="bg-white text-black px-6 py-3 rounded-md hover:bg-gray-200 transition-colors"
        >
          กลับไปหน้าสินค้า
        </NuxtLink>
      </div>
    </div>

    <!-- Product Detail Content -->
    <div v-else-if="product" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb -->
      <nav class="mb-8">
        <ol class="flex items-center space-x-2 text-sm text-gray-400">
          <li><NuxtLink to="/" class="hover:text-white">หน้าแรก</NuxtLink></li>
          <li><span class="mx-2">/</span></li>
          <li><NuxtLink to="/products" class="hover:text-white">สินค้า</NuxtLink></li>
          <li><span class="mx-2">/</span></li>
          <li v-if="product.category">
            <NuxtLink :to="`/categories?category=${product.category.id}`" class="hover:text-white">
              {{ product.category.name }}
            </NuxtLink>
          </li>
          <li><span class="mx-2">/</span></li>
          <li class="text-white">{{ product.name }}</li>
        </ol>
      </nav>

      <!-- Product Details -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Product Images -->
        <div class="space-y-4">
          <!-- Main Image -->
          <div class="aspect-square bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg flex items-center justify-center overflow-hidden">
            <img
              v-if="product.images && product.images.length > 0 && selectedImage"
              :src="selectedImage"
              :alt="product.name"
              class="w-full h-full object-cover"
              @error="onImageError"
            />
            <div v-else class="text-gray-500 text-center">
              <svg class="w-24 h-24 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="text-gray-400">ไม่มีรูปภาพ</p>
            </div>
          </div>
          
          <!-- Image Thumbnails -->
          <div v-if="product.images && product.images.length > 1" class="grid grid-cols-4 gap-2">
            <div
              v-for="(image, index) in product.images"
              :key="index"
              class="aspect-square bg-gray-800 rounded-md overflow-hidden cursor-pointer border-2 transition-all"
              :class="selectedImage === image ? 'border-white' : 'border-gray-700 hover:border-gray-500'"
              @click="selectedImage = image"
            >
              <img
                :src="image"
                :alt="`${product.name} - รูปที่ ${index + 1}`"
                class="w-full h-full object-cover"
                @error="onImageError"
              />
            </div>
          </div>
        </div>

        <!-- Product Information -->
        <div class="space-y-6">
          <!-- Product Title and Rating -->
          <div>
            <h1 class="text-3xl font-bold text-white mb-4">{{ product.name }}</h1>
            
            <!-- Rating and Reviews -->
            <div class="flex items-center space-x-4 mb-4">
              <div class="flex items-center">
                <div class="flex text-yellow-400">
                  <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= product.rating ? 'text-yellow-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
                <span class="text-white ml-2 font-semibold">{{ product.rating.toFixed(1) }}</span>
                <span class="text-gray-400 ml-2">({{ product.review_count }} รีวิว)</span>
              </div>
            </div>

            <!-- Category and Brand -->
            <div class="flex items-center space-x-4 text-sm text-gray-400">
              <span v-if="product.category">หมวดหมู่: <span class="text-white">{{ product.category.name }}</span></span>
              <span v-if="product.brand">แบรนด์: <span class="text-white">{{ product.brand }}</span></span>
              <span v-if="product.sku">รหัสสินค้า: <span class="text-white">{{ product.sku }}</span></span>
            </div>
          </div>

          <!-- Price -->
          <div class="border-t border-gray-800 pt-6">
            <div class="flex items-center space-x-4 mb-4">
              <span class="text-4xl font-bold text-white">฿{{ formatPrice(product.price) }}</span>
              <span v-if="product.original_price && product.original_price > product.price" class="text-xl text-gray-400 line-through">
                ฿{{ formatPrice(product.original_price) }}
              </span>
              <span v-if="product.original_price && product.original_price > product.price" class="bg-red-600 text-white px-2 py-1 rounded text-sm">
                ประหยัด {{ Math.round(((product.original_price - product.price) / product.original_price) * 100) }}%
              </span>
            </div>
            
            <!-- Stock Status -->
            <div class="flex items-center space-x-2 mb-6">
              <span class="text-sm text-gray-400">สถานะสินค้า:</span>
              <span v-if="product.stock_quantity > 0" class="text-green-400 font-semibold">
                มีสินค้า ({{ product.stock_quantity }} ชิ้น)
              </span>
              <span v-else class="text-red-400 font-semibold">หมดสินค้า</span>
            </div>
          </div>

          <!-- Add to Cart Section -->
          <div class="border-t border-gray-800 pt-6">
            <div class="flex items-center space-x-4 mb-6">
              <div class="flex items-center space-x-2">
                <label class="text-sm text-gray-400">จำนวน:</label>
                <div class="flex items-center border border-gray-600 rounded-md">
                  <button
                    @click="decreaseQuantity"
                    :disabled="quantity <= 1"
                    class="px-3 py-2 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    -
                  </button>
                  <input
                    v-model.number="quantity"
                    type="number"
                    min="1"
                    :max="product.stock_quantity"
                    class="w-16 px-2 py-2 text-center bg-transparent text-white border-0 focus:outline-none"
                  />
                  <button
                    @click="increaseQuantity"
                    :disabled="quantity >= product.stock_quantity"
                    class="px-3 py-2 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            <div class="flex space-x-4">
              <button
                @click="addToCart"
                :disabled="product.stock_quantity === 0 || adding"
                class="flex-1 bg-white text-black px-6 py-3 rounded-md font-semibold hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="adding">กำลังเพิ่ม...</span>
                <span v-else-if="product.stock_quantity > 0">เพิ่มลงตะกร้า</span>
                <span v-else>หมดสินค้า</span>
              </button>
              
              <button
                @click="toggleWishlist"
                class="px-6 py-3 border border-gray-600 rounded-md hover:border-white transition-colors"
              >
                <svg class="w-6 h-6" :class="isInWishlist ? 'text-red-500' : 'text-gray-400'" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Product Tags -->
          <div v-if="product.tags && product.tags.length > 0" class="border-t border-gray-800 pt-6">
            <h3 class="text-sm text-gray-400 mb-2">แท็ก:</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in product.tags"
                :key="tag"
                class="px-3 py-1 bg-gray-800 text-gray-300 rounded-full text-sm"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Product Description -->
      <div class="mt-12">
        <div class="border-t border-gray-800 pt-8">
          <h2 class="text-2xl font-bold text-white mb-6">รายละเอียดสินค้า</h2>
          <div class="prose prose-invert max-w-none">
            <p class="text-gray-300 leading-relaxed whitespace-pre-line">{{ product.description || 'ไม่มีรายละเอียดสินค้า' }}</p>
          </div>
        </div>
      </div>

      <!-- Related Products -->
      <div v-if="relatedProducts.length > 0" class="mt-16">
        <div class="border-t border-gray-800 pt-8">
          <h2 class="text-2xl font-bold text-white mb-8">สินค้าที่เกี่ยวข้อง</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              v-for="relatedProduct in relatedProducts"
              :key="relatedProduct.id"
              class="bg-black border border-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform duration-300 cursor-pointer"
              @click="viewProduct(relatedProduct.id)"
            >
              <!-- Product Image -->
              <div class="h-48 bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
                <svg class="w-16 h-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              
              <!-- Product Info -->
              <div class="p-4">
                <h3 class="text-lg font-semibold text-white mb-2 line-clamp-2">{{ relatedProduct.name }}</h3>
                <div class="flex items-center justify-between">
                  <span class="text-xl font-bold text-white">฿{{ formatPrice(relatedProduct.price) }}</span>
                  <div class="flex text-yellow-400">
                    <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= relatedProduct.rating ? 'text-yellow-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-black border-t border-gray-800 mt-20">
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

// Import components
import ProfileDropdown from '~/components/ProfileDropdown.vue'

const route = useRoute()
const router = useRouter()
const { apiCall } = useApi()
const { addItem, fetchCart } = useCart()

// Reactive data
const product = ref(null)
const relatedProducts = ref([])
const loading = ref(true)
const error = ref(null)
const selectedImage = ref(null)
const quantity = ref(1)
const adding = ref(false)
const isInWishlist = ref(false)

// Authentication state
const isLoggedIn = ref(false)
const currentUser = ref(null)

// Get product ID from route
const productId = computed(() => route.params.id)

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

// Handle logout
const handleLogout = () => {
  isLoggedIn.value = false
  currentUser.value = null
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('hasVisitedBefore')
  navigateTo('/login')
}

// Fetch product details
const fetchProduct = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await apiCall(`/api/products/${productId.value}`)
    
    if (response.success) {
      product.value = response.product
      selectedImage.value = product.value.images?.[0] || null
      
      // Fetch related products
      await fetchRelatedProducts()
    } else {
      error.value = response.error || 'ไม่พบสินค้า'
    }
  } catch (err) {
    console.error('Error fetching product:', err)
    error.value = 'เกิดข้อผิดพลาดในการโหลดข้อมูลสินค้า'
  } finally {
    loading.value = false
  }
}

// Fetch related products
const fetchRelatedProducts = async () => {
  try {
    const response = await apiCall(`/api/products/${productId.value}/related`)
    
    if (response.success) {
      relatedProducts.value = response.products
    }
  } catch (err) {
    console.error('Error fetching related products:', err)
  }
}

// Quantity controls
const increaseQuantity = () => {
  if (quantity.value < product.value.stock_quantity) {
    quantity.value++
  }
}

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--
  }
}

// Add to cart
const addToCart = async () => {
  if (!isLoggedIn.value) {
    navigateTo('/login')
    return
  }

  try {
    adding.value = true
    await addItem(product.value.id, quantity.value)
    await fetchCart()
    
    // Show success message (you can implement a toast/notification here)
    console.log('เพิ่มสินค้าลงตะกร้าเรียบร้อยแล้ว')
  } catch (err) {
    console.error('Error adding to cart:', err)
    // Show error message
  } finally {
    adding.value = false
  }
}

// Toggle wishlist (placeholder function)
const toggleWishlist = () => {
  isInWishlist.value = !isInWishlist.value
  // TODO: Implement wishlist functionality
}

// Navigate to product
const viewProduct = (id) => {
  navigateTo(`/products/${id}`)
}

// Handle image error
const onImageError = (event) => {
  event.target.style.display = 'none'
}

// Format price
const formatPrice = (price) => {
  return price.toLocaleString('th-TH')
}

// Watch route changes
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchProduct()
  }
})

// Lifecycle
onMounted(async () => {
  checkAuthStatus()
  await fetchProduct()
})

// Update document title
useHead({
  title: computed(() => product.value ? `${product.value.name} - ShopHub` : 'รายละเอียดสินค้า - ShopHub'),
  meta: [
    {
      name: 'description',
      content: computed(() => product.value ? product.value.description : 'รายละเอียดสินค้า')
    }
  ]
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

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

/* Number input styling */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
