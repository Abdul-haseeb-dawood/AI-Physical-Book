// Chat API service to connect frontend to backend
class ChatAPI {
  constructor(baseURL = process.env.REACT_APP_API_BASE_URL ? `${process.env.REACT_APP_API_BASE_URL}/api` : '/api') {
    this.baseURL = baseURL;
  }

  async sendMessage(query, context = {}) {
    try {
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          ...context
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async sendSelectedTextMessage(query, selectedText, context = {}) {
    try {
      const response = await fetch(`${this.baseURL}/chat/selected-text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          selected_text: selectedText,
          ...context
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending selected text message:', error);
      throw error;
    }
  }

  // Method to pass page/chapter context with queries
  getPageContext() {
    return {
      page: window.location.pathname,
      chapter: document.querySelector('h1')?.textContent || 'Unknown Chapter',
    };
  }
}

export default new ChatAPI();