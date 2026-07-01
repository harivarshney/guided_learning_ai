/**
 * Home Page Component
 * Main page for asking questions
 */

import React, { useState } from 'react';
import { askQuestion } from '../api/client';
import QuestionInput from '../components/QuestionInput';
import ResponseDisplay from '../components/ResponseDisplay';
import './HomePage.css';

function Home({ userId }) {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAskQuestion = async (questionText) => {
    if (!questionText.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await askQuestion(questionText, userId);
      setResponse(result.data);
      setQuestion('');
    } catch (err) {
      setError('Failed to process question. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="homepage">
      <div className="homepage-container">
        <div className="welcome-section">
          <h1>🎓 Ask Your Learning Questions</h1>
          <p>Get personalized explanations, resources, and guidance to help you learn.</p>
        </div>

        <QuestionInput
          question={question}
          setQuestion={setQuestion}
          onAsk={handleAskQuestion}
          loading={loading}
        />

        {error && <div className="error-message">{error}</div>}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing your question and finding resources...</p>
          </div>
        )}

        {response && <ResponseDisplay response={response} />}
      </div>
    </div>
  );
}

export default Home;