import React, { useState } from 'react';

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSendMessage = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-input-area">
      <textarea
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask about the book content..."
        rows="1"
        disabled={isLoading}
      />
      <button 
        onClick={handleSendMessage} 
        disabled={!inputValue.trim() || isLoading}
        className="send-button"
      >
        Send
      </button>
    </div>
  );
};

export default ChatInput;