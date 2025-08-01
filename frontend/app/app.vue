<template>
  <div class="grid justify-center items-center bg-[#0C2D71]">
    <div class="min-h-screen flex flex-col items-start justify-center text-white text-start px-4">
      <!-- Приветствие -->
      <div class="space-y-6">
        <div class="border-0 w-10 h-10 rounded-lg bg-blue-600 text-white flex items-center justify-center">
          <Icon name="fa6-solid:comment" class="w-6 h-6" />
        </div>
        <div class="text-3xl font-semibold">Hi there!</div>
        <div class="text-4xl font-bold">What would you like to know?</div>
        <p class="text-base text-white/70">Use one of the most common prompts below<br />or ask your own question</p>
      </div>

      <!-- Ответ -->
      <div v-if="reply || loading" class="mt-10 max-w-xl w-full">
        <div class="bg-white text-black rounded-lg p-4 whitespace-pre-wrap leading-relaxed">
          <div v-if="loading" class="text-blue-600 animate-pulse">Thinking<span class="dots"></span></div>
          <div v-else v-html="parseMarkdown(reply)" class="text-blue-800" />
        </div>
      </div>

      <!-- Ошибка -->
      <div v-if="error" class="text-red-400 mt-4 max-w-xl">{{ error }}</div>

      <!-- Поле ввода -->
      <div class="mt-10 w-full max-w-xl mx-auto">
        <ChatInput v-model="text" @send="send" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ChatInput from '../components/ChatInput.vue'
import { useChat } from '../composables/useChat'
import { marked } from 'marked';

marked.setOptions({
  breaks: true,
  gfm: true,
  sanitize: true
});

const parseMarkdown = (text) => {
  return marked.parse(text || '');
};

const { text, reply, loading, error, send } = useChat()
</script>

<style scoped>
.dots::after {
  content: '...';
  animation: dots 1.5s steps(3, end) infinite;
}

@keyframes dots {
  0% {
    content: '';
  }

  33% {
    content: '.';
  }

  66% {
    content: '..';
  }

  100% {
    content: '...';
  }
}
</style>