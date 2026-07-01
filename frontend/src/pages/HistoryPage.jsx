/**
 * HistoryPage Component
 * Shows all previous questions asked by the user
 * Click any question to view the full response in a modal
 */

import React, { useState, useEffect } from 'react';
import { getUserHistory } from '../api/client';
import ResponseModal from '../components/ResponseModal';
import './HistoryPage.css';

function HistoryPage({ userId }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedResponse, setSelectedResponse] = useState(null);
  const [responseLoading, setResponseLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const data = await getUserHistory(userId);
      setHistory(data.questions || []);
    } catch (err) {
      setError('Failed to load history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuestionClick = async (historyItem) => {
    try {
      setResponseLoading(true);
      
      // Use response_data from the history item
      if (historyItem.response_data) {
        setSelectedResponse(historyItem.response_data);
      } else {
        alert('No response data available for this question');
      }
    } catch (err) {
      console.error('Error loading response:', err);
      alert('Failed to load full response');
    } finally {
      setResponseLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="history-page">
      <div className="history-container">
        <h1>📚 Your Learning History</h1>
        <p>Click any question to review the full learning response</p>

        {loading && <div className="loading">Loading history...</div>}
        {error && <div className="error-message">{error}</div>}

        {!loading && history.length === 0 && (
          <div className="empty-state">
            <p>No questions yet. Start asking!</p>
          </div>
        )}

        {!loading && history.length > 0 && (
          <div className="history-list">
            <p className="total-questions">Total: {history.length} questions</p>
            {history.map((item) => (
              <div
                key={item.id}
                className="history-card clickable"
                onClick={() => handleQuestionClick(item)}
              >
                <div className="history-header">
                  <h3>{item.question}</h3>
                  <span className="history-date">{formatDate(item.created_at)}</span>
                </div>
                <div className="history-meta">
                  <span className="concept-badge">{item.concept}</span>
                  <span className={`difficulty-badge difficulty-${item.difficulty_level}`}>
                    {item.difficulty_level}
                  </span>
                </div>
                {item.context && (
                  <p className="history-context">Context: {item.context}</p>
                )}
                <div className="click-hint">Click to view full response →</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Response Modal */}
      {selectedResponse && !responseLoading && (
        <ResponseModal
          response={selectedResponse}
          onClose={() => setSelectedResponse(null)}
        />
      )}

      {responseLoading && (
        <div className="modal-overlay">
          <div className="loading">Loading response...</div>
        </div>
      )}
    </div>
  );
}

export default HistoryPage;