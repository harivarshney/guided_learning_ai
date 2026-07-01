/**
 * ProgressPage Component
 * Shows user's learning progress and statistics
 */

import React, { useState, useEffect } from 'react';
import { getUserProgress } from '../api/client';
import './ProgressPage.css';

function ProgressPage({ userId }) {
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchProgress();
  }, [userId]);

  const fetchProgress = async () => {
    try {
      setLoading(true);
      const data = await getUserProgress(userId);
      setProgress(data.progress || []);
    } catch (err) {
      setError('Failed to load progress');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getProgressPercentage = (understanding_level) => {
    return Math.min(100, Math.max(0, understanding_level));
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <div className="progress-page">
      <div className="progress-container">
        <h1>📈 Your Learning Progress</h1>
        <p>Track your mastery across different concepts</p>

        {loading && <div className="loading">Loading progress...</div>}
        {error && <div className="error-message">{error}</div>}

        {!loading && progress.length === 0 && (
          <div className="empty-state">
            <p>No progress yet. Ask questions to start tracking!</p>
          </div>
        )}

        {!loading && progress.length > 0 && (
          <div className="progress-grid">
            <div className="progress-stats">
              <div className="stat-card">
                <h3>{progress.length}</h3>
                <p>Concepts Learned</p>
              </div>
              <div className="stat-card">
                <h3>{progress.reduce((sum, p) => sum + p.times_asked, 0)}</h3>
                <p>Total Questions Asked</p>
              </div>
              <div className="stat-card">
                <h3>{Math.round(progress.reduce((sum, p) => sum + p.understanding_level, 0) / progress.length)}%</h3>
                <p>Average Understanding</p>
              </div>
              <div className="stat-card">
                <h3>{progress.reduce((sum, p) => sum + p.practice_completed, 0)}</h3>
                <p>Problems Completed</p>
              </div>
            </div>

            <div className="progress-list">
              {progress.map((item) => (
                <div key={item.id} className="progress-card">
                  <div className="progress-header">
                    <h3>{item.concept}</h3>
                    <span className="times-asked">Asked {item.times_asked}x</span>
                  </div>

                  <div className="progress-bar-container">
                    <div className="progress-bar-label">
                      <span>Understanding Level</span>
                      <span className="percentage">{Math.round(item.understanding_level)}%</span>
                    </div>
                    <div className="progress-bar">
                      <div
                        className="progress-bar-fill"
                        style={{ width: `${getProgressPercentage(item.understanding_level)}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="progress-details">
                    <div className="detail-item">
                      <span className="label">Last Asked:</span>
                      <span className="value">{formatDate(item.last_asked)}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">Practice Problems:</span>
                      <span className="value">{item.practice_completed}</span>
                    </div>
                  </div>

                  {item.notes && (
                    <div className="progress-notes">
                      <strong>Notes:</strong> {item.notes}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProgressPage;