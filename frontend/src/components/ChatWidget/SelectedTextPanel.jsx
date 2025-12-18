import React, { useState } from 'react';
import './SelectedTextPanel.css';

const SelectedTextPanel = ({ selectedText, onAskQuestion, onClose }) => {
  const [question, setQuestion] = useState('');

  const handleAsk = () => {
    if (question.trim() && selectedText) {
      onAskQuestion(question, selectedText);
      setQuestion('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  if (!selectedText) return null;

  return (
    <div className="selected-text-panel">
      <div className="panel-header">
        <h4>Ask about selected text:</h4>
        <button className="close-panel" onClick={onClose}>×</button>
      </div>
      <div className="selected-content">
        "{selectedText}"
      </div>
      <div className="question-input">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="What would you like to know about this text?"
          rows="2"
        />
        <button onClick={handleAsk} disabled={!question.trim()}>
          Ask Question
        </button>
      </div>
    </div>
  );
};

export default SelectedTextPanel;