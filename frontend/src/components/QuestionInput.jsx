/**
 * QuestionInput Component
 * Form for entering questions
 */

import React from 'react';
import './QuestionInput.css';

function QuestionInput({ question, setQuestion, onAsk, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onAsk(question);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey && !loading) {
      handleSubmit(e);
    }
  };

  return (
    <form className="question-input-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <textarea
          className="question-textarea"
          placeholder="What would you like to learn about? Ask any question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
          rows="4"
        />
      </div>

      <div className="input-footer">
        <small>Press Ctrl+Enter or click Ask to submit</small>
        <button
          type="submit"
          className="ask-button"
          disabled={loading || !question.trim()}
        >
          {loading ? 'Processing...' : '✨ Ask Question'}
        </button>
      </div>
    </form>
  );
}

export default QuestionInput;