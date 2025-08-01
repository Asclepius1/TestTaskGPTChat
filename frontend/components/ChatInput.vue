<template>
    <span class="hidden text-blue-700 text-blue-600"></span>
    <div
        class="flex items-center justify-center bg-[#0C2D71] backdrop-blur-sm rounded-xl pl-3 border-blue-600 border-2 overflow-hidden">
        <button @click="toggleRecording" class="mr-4 transition"
            :class="isListening ? 'text-blue-700' : 'text-blue-600'" aria-label="Toggle voice recognition">
            <Icon :name="isListening ? 'fa6-solid:microphone-slash' : 'fa6-solid:microphone'" class="block h-5 w-5" />
        </button>

        <input v-model="inputText" type="text" :placeholder="isListening ? 'Listening...' : 'Ask whatever you want'"
            class="flex-grow bg-transparent focus:outline-none text-white placeholder-white/70 text-lg"
            @keyup.enter="emitSend" />
        <button @click="emitSend"
            class="ml-4 bg-blue-700 hover:bg-blue-800 p-2 rounded-l-lg transition flex items-center justify-center"
            aria-label="Send message">
            <Icon name="fa6-solid:angle-right" class="h-6 w-6 text-white" />
        </button>
    </div>
</template>

<script setup>
import { watch, ref } from 'vue'
import { useSpeechRecognition } from '../composables/useSpeechRecognition'

const props = defineProps({
    modelValue: String
})

const emit = defineEmits(['update:modelValue', 'send'])

// Работа с распознаванием речи
const { transcript, isListening, toggle: toggleRecording } = useSpeechRecognition('en-US')

// Состояние поля ввода
const inputText = ref(props.modelValue)

// Следим за `modelValue` от родителя
watch(
    () => props.modelValue,
    (val) => {
        inputText.value = val
    }
)

// Если речь распознана — вставляем её в поле и эмитим в родитель
watch(transcript, (t) => {
    if (t) {
        inputText.value = t
        emit('update:modelValue', t)
    }
})

// При вводе вручную — синхронизируем с родителем
watch(inputText, (val) => {
    emit('update:modelValue', val)
})

function emitSend() {
    emit('send')
}
</script>