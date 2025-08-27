<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <NuxtLink 
              to="/admin/dashboard"
              class="text-gray-500 hover:text-gray-700"
            >
              ← Dashboard
            </NuxtLink>
            <h1 class="text-2xl font-bold text-gray-900">จัดการผู้ใช้</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">{{ user?.username || 'Admin' }}</span>
            <button
              @click="logout"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              ออกจากระบบ
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Search and Filters -->
      <div class="bg-white shadow rounded-lg p-6 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div class="mb-4 sm:mb-0">
            <input
              v-model="searchQuery"
              @input="debouncedSearch"
              type="text"
              placeholder="ค้นหาผู้ใช้..."
              class="w-full sm:w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
            />
          </div>
          <div class="text-sm text-gray-500">
            ทั้งหมด {{ pagination?.total || 0 }} คน
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
        <p class="text-red-600">{{ error }}</p>
        <button
          @click="fetchUsers"
          class="mt-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm"
        >
          ลองใหม่
        </button>
      </div>

      <!-- Users Table -->
      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ผู้ใช้
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ชื่อ-นามสกุล
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  สถานะ
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  สมัครเมื่อ
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  การจัดการ
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="userItem in users" :key="userItem.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">
                    {{ userItem.username }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{ userItem.first_name }} {{ userItem.last_name }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="userItem.is_admin ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'"
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                  >
                    {{ userItem.is_admin ? 'ผู้ดูแล' : 'ผู้ใช้ทั่วไป' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(userItem.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    @click="toggleAdminStatus(userItem)"
                    :disabled="updatingUser === userItem.id"
                    :class="userItem.is_admin ? 'text-red-600 hover:text-red-900' : 'text-blue-600 hover:text-blue-900'"
                    class="disabled:opacity-50"
                  >
                    {{ updatingUser === userItem.id ? 'กำลังอัปเดต...' : (userItem.is_admin ? 'ลบสิทธิ์ผู้ดูแล' : 'เลื่อนเป็นผู้ดูแล') }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-if="users.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">ไม่พบผู้ใช้</h3>
          <p class="mt-1 text-sm text-gray-500">ไม่มีผู้ใช้ในระบบ</p>
        </div>

        <!-- Pagination -->
        <div v-if="pagination && pagination.pages > 1" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="changePage(pagination.page - 1)"
              :disabled="pagination.page <= 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              ก่อนหน้า
            </button>
            <button
              @click="changePage(pagination.page + 1)"
              :disabled="pagination.page >= pagination.pages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              ถัดไป
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                แสดง {{ ((pagination.page - 1) * pagination.limit) + 1 }} ถึง {{ Math.min(pagination.page * pagination.limit, pagination.total) }} จาก {{ pagination.total }} รายการ
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="changePage(pagination.page - 1)"
                  :disabled="pagination.page <= 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  ก่อนหน้า
                </button>
                <template v-for="page in getPages()" :key="page">
                  <button
                    v-if="page !== '...'"
                    @click="changePage(page)"
                    :class="page === pagination.page ? 'bg-black text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium"
                  >
                    {{ page }}
                  </button>
                  <span v-else class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                    ...
                  </span>
                </template>
                <button
                  @click="changePage(pagination.page + 1)"
                  :disabled="pagination.page >= pagination.pages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  ถัดไป
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// Meta tags
useHead({
  title: 'จัดการผู้ใช้ - Admin Dashboard',
  meta: [
    { name: 'description', content: 'User management page for ShopHub admin' }
  ]
})

// Define page meta
definePageMeta({
  layout: false,
  middleware: 'admin-auth'
})

// Reactive state
const users = ref([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const pagination = ref(null)
const updatingUser = ref(null)

// Composables
const { apiCall } = useApi()
const router = useRouter()

// Get user from cookie
const user = useCookie('auth-user')

// Debounced search
const debouncedSearch = debounce(() => {
  currentPage.value = 1
  fetchUsers()
}, 500)

// Methods
const fetchUsers = async () => {
  loading.value = true
  error.value = ''

  try {
    const token = useCookie('auth-token')
    
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      limit: '20'
    })
    
    if (searchQuery.value.trim()) {
      params.append('search', searchQuery.value.trim())
    }

    const response = await apiCall(`/api/admin/users?${params}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })

    users.value = response.users
    pagination.value = response.pagination
  } catch (err) {
    console.error('Users fetch error:', err)
    error.value = err.message || 'เกิดข้อผิดพลาดในการโหลดข้อมูลผู้ใช้'
  } finally {
    loading.value = false
  }
}

const toggleAdminStatus = async (userItem) => {
  if (updatingUser.value) return
  
  // Confirm action
  const action = userItem.is_admin ? 'ลบสิทธิ์ผู้ดูแล' : 'เลื่อนเป็นผู้ดูแล'
  if (!confirm(`คุณแน่ใจหรือไม่ที่จะ${action}สำหรับ ${userItem.username}?`)) {
    return
  }

  updatingUser.value = userItem.id

  try {
    const token = useCookie('auth-token')
    
    const response = await apiCall(`/api/admin/users/${userItem.id}/toggle-admin`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })

    // Update user in the list
    const userIndex = users.value.findIndex(u => u.id === userItem.id)
    if (userIndex !== -1) {
      users.value[userIndex].is_admin = response.user.is_admin
    }

    // Show success message (you could use a toast notification here)
    alert(response.message)

  } catch (err) {
    console.error('Toggle admin status error:', err)
    alert(err.message || 'เกิดข้อผิดพลาดในการอัปเดตสถานะ')
  } finally {
    updatingUser.value = null
  }
}

const changePage = (page) => {
  if (page >= 1 && page <= pagination.value.pages) {
    currentPage.value = page
    fetchUsers()
  }
}

const getPages = () => {
  const pages = []
  const total = pagination.value.pages
  const current = pagination.value.page

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    }
  }
  
  return pages
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const logout = () => {
  const token = useCookie('auth-token')
  const userData = useCookie('auth-user')
  
  token.value = null
  userData.value = null
  
  router.push('/admin/login')
}

// Utility function for debouncing
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Fetch data on component mount
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
