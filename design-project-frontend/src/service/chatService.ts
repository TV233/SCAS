import axios from 'axios';

const chatApi = axios.create({
  headers: {
    'Content-Type': 'application/json'
  }
});

export const sendChatMessage = async (messages: Array<{role: string; content: string}>, onMessage: (message: string) => void) => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'llama3.2',
        messages,
        stream: true
      })
    });

    if (!response.body) {
      throw new Error('ReadableStream not supported in this browser.');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    const processJSON = (jsonStr: string) => {
      try {
        const json = JSON.parse(jsonStr);
        if (json.message?.content) {
          onMessage(json.message.content);
        }
      } catch (e) {
        console.error('Error parsing JSON:', e);
      }
    };

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      buffer += chunk;

      // 查找完整的JSON对象
      let startIndex = 0;
      let endIndex = buffer.indexOf('}\n', startIndex);

      while (endIndex !== -1) {
        const jsonStr = buffer.substring(startIndex, endIndex + 1);
        processJSON(jsonStr);

        startIndex = endIndex + 2; // 跳过 '}\n'
        endIndex = buffer.indexOf('}\n', startIndex);
      }

      // 保留未处理的部分
      buffer = buffer.substring(startIndex);
    }

    // 处理最后可能剩余的数据
    if (buffer.trim()) {
      processJSON(buffer);
    }
  } catch (error) {
    console.error('Chat API error:', error);
    throw error;
  }
};
