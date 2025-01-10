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
      } catch (error) {
        // 尝试处理不完整的JSON
        const lastNewline = buffer.lastIndexOf('\n');
        if (lastNewline !== -1) {
          const completeJson = buffer.substring(0, lastNewline);
          buffer = buffer.substring(lastNewline + 1);

          completeJson.split('\n').forEach(line => {
            if (line.trim()) {
              try {
                const json = JSON.parse(line);
                if (json.message?.content) {
                  onMessage(json.message.content);
                }
              } catch (parseError) {
                console.error('Error parsing JSON line:', parseError);
              }
            }
          });
        }
      }
    };

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      buffer += chunk;

      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // 保留最后一个可能不完整的行

      for (const line of lines) {
        if (line.trim()) {
          processJSON(line);
        }
      }
    }

    if (buffer.trim()) {
      processJSON(buffer);
    }
  } catch (error) {
    console.error('Chat API error:', error);
    throw error;
  }
};
