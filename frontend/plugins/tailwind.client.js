export default defineNuxtPlugin(() => {
  // Load Tailwind CSS on client side
  if (process.client) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = '/tailwind.css'
    document.head.appendChild(link)
  }
})
