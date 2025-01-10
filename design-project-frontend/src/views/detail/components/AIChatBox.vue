<template>
  <div v-show="visible" class="chat-container">
    <div class="chat-header">
      <span>AI 股票助手</span>
      <AButton type="text" @click="$emit('close')">
        <icon-material-symbols:close />
      </AButton>
    </div>

    <div class="chat-messages" ref="messagesRef">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role === 'assistant' ? 'assistant' : 'user']"
      >
        {{ msg.content }}
      </div>
    </div>

    <div class="chat-input">
      <AInput
        v-model:value="inputMessage"
        placeholder="请输入您的问题..."
        @keyup.enter="sendMessage"
      />
      <AButton type="primary" @click="sendMessage" :loading="loading">
        发送
      </AButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import { sendChatMessage } from '@/service/chatService';

const props = defineProps<{
  visible: boolean;
}>();

const emit = defineEmits(['close']);

const inputMessage = ref('');
const messages = ref<Array<{role: string; content: string}>>([]);
const loading = ref(false);
const messagesRef = ref<HTMLDivElement>();

const scrollToBottom = async () => {
  await nextTick();
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
  }
};

const initChat = async () => {
  loading.value = true;
  try {
    let assistantMessage = { role: 'assistant', content: '' };
    messages.value.push(assistantMessage);

    await sendChatMessage([{
      role: 'user',
      content: '你是一个股票分析专家，你可以为用户提供股票分析建议，请为用户提供股票分析支持。当你准备好了，请说"您好，请问您有什么股票投资问题？"'
    }], (chunk) => {
      assistantMessage.content += chunk;
    });

    await scrollToBottom();
  } catch (error) {
    console.error('初始化聊天失败:', error);
  } finally {
    loading.value = false;
  }
};

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return;

  const userMessage = inputMessage.value;
  messages.value.push({
    role: 'user',
    content: userMessage
  });

  inputMessage.value = '';
  loading.value = true;

  try {
    let assistantMessage = { role: 'assistant', content: '' };
    messages.value.push(assistantMessage);

    await sendChatMessage([...messages.value], (chunk) => {
      assistantMessage.content += chunk;
    });

    await scrollToBottom();
  } catch (error) {
    console.error('发送消息失败:', error);
  } finally {
    loading.value = false;
  }
};

watch(() => props.visible, (newVal) => {
  if (newVal && messages.value.length === 0) {
    initChat();
  }
});

onMounted(() => {
  if (props.visible) {
    initChat();
  }
});
</script>

<style scoped>
.chat-container {
  position: fixed;
  right: 20px;
  bottom: 20px;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.chat-header {
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  max-width: 80%;
  word-break: break-word;
}

.user {
  background: #e3f2fd;
  margin-left: auto;
}

.assistant {
  background: #f5f5f5;
  margin-right: auto;
}

.chat-input {
  padding: 10px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
}
</style>
