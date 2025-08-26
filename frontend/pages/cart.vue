<template>
  <div class="min-h-screen bg-black text-white">
    <header class="bg-black border-b border-gray-800 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-2xl font-bold text-white">ShopHub</NuxtLink>
        <NuxtLink to="/products" class="text-gray-300 hover:text-white">กลับไปช้อปต่อ</NuxtLink>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold mb-6">ตะกร้าสินค้า</h1>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-4">
          <div v-if="items.length === 0" class="p-6 border border-gray-800 rounded-lg text-center text-gray-300">
            ไม่มีสินค้าในตะกร้า
          </div>

          <div v-for="it in items" :key="it.product.id" class="p-4 border border-gray-800 rounded-lg flex gap-4 items-center">
            <div class="w-20 h-20 bg-gray-800 rounded flex items-center justify-center">
              <svg class="w-10 h-10 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="flex justify-between items-start">
                <div>
                  <p class="font-semibold">{{ it.product.name }}</p>
                  <p class="text-gray-400 text-sm">฿{{ formatPrice(it.price_at_add) }}</p>
                </div>
                <button class="text-gray-400 hover:text-white" @click="remove(it.product.id)">ลบ</button>
              </div>
              <div class="mt-3 flex items-center gap-2">
                <button class="px-3 py-1 border border-gray-700 rounded" @click="decrease(it)">-</button>
                <input class="w-16 text-center bg-gray-900 border border-gray-700 rounded py-1" :value="it.quantity" @change="(e)=>changeQty(it, e.target.value)" />
                <button class="px-3 py-1 border border-gray-700 rounded" @click="increase(it)">+</button>
              </div>
            </div>
          </div>
        </div>

        <div class="border border-gray-800 rounded-lg p-6 h-fit sticky top-24">
          <h2 class="text-xl font-semibold mb-4">สรุปคำสั่งซื้อ</h2>
          <div class="flex justify-between text-gray-300 mb-2">
            <span>ยอดรวมสินค้า</span>
            <span>฿{{ formatPrice(totals.subtotal) }}</span>
          </div>
          <div class="flex justify-between text-gray-300 mb-6">
            <span>จำนวนสินค้า</span>
            <span>{{ totals.total_quantity }}</span>
          </div>
          <button :disabled="items.length===0" class="w-full bg-white text-black py-2 rounded-md hover:bg-gray-200 disabled:opacity-50">ชำระเงิน</button>
        </div>
      </div>
    </main>
  </div>
  
</template>

<script setup>
definePageMeta({ layout: 'default' })
const { items, totals, loading, fetchCart, updateItem, removeItem } = useCart()

const formatPrice = (p) => Number(p || 0).toLocaleString('th-TH')

const decrease = async (it) => {
  const q = Math.max(1, (it.quantity || 1) - 1)
  await updateItem(it.product.id, q)
}
const increase = async (it) => {
  const q = (it.quantity || 1) + 1
  await updateItem(it.product.id, q)
}
const changeQty = async (it, v) => {
  const q = Math.max(1, parseInt(v || '1', 10))
  await updateItem(it.product.id, q)
}
const remove = async (productId) => {
  await removeItem(productId)
}

onMounted(() => fetchCart())
</script>


