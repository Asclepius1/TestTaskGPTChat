import { useRuntimeConfig, useFetch } from '#imports'
import { ref } from 'vue'

export function useChat() {
  const text = ref('')
  const reply = ref('')
  const loading = ref(false)
  const error = ref<string | null>(null)

  const config = useRuntimeConfig()

  async function send() {
    if (!text.value.trim()) return
    loading.value = true
    error.value = null
    try {
      const { data, error: fetchError } = await useFetch('/api/chat', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { text: text.value },
      })
      if (fetchError.value) throw fetchError.value
      reply.value = data.value.reply
    } catch (e: any) {
      error.value = e.data.detail || 'An error occurred while sending the message.'
      reply.value = ''
    } finally {
      loading.value = false
    }
  }

  return { text, reply, loading, error, send }
}
