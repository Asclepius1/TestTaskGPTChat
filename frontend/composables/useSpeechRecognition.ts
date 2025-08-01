import { ref, onMounted } from 'vue';
export function useSpeechRecognition(lang = 'en-US') {
  const isListening = ref(false);
  const transcript = ref('');
  const error = ref('');
  let recognition: SpeechRecognition | null = null;

  onMounted(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) {
      error.value = 'Speech recognition not supported';
      return;
    }
    recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = lang;
    recognition.onresult = event => {
      transcript.value = event.results[0][0].transcript;
      isListening.value = false;
    };
    recognition.onerror = event => {
      error.value = event.error;
      isListening.value = false;
    };
    recognition.onend = () => {
      if (isListening.value) recognition!.start();
    };
  });

  function toggle() {
    if (!recognition) return;
    if (isListening.value) {
      recognition.stop();
      isListening.value = false;
    } else {
      recognition.start();
      isListening.value = true;
    }
  }

  return { transcript, isListening, error, toggle };
}