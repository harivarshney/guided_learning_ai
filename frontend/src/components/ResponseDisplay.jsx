/**
 * ResponseDisplay Component
 * Shows AI responses from all agents
 * Includes downloadable study questions
 */

import React, { useState } from 'react';
import './ResponseDisplay.css';

function ResponseDisplay({ response }) {
  const [activeTab, setActiveTab] = useState('analysis');

  if (!response || !response.agents) {
    return null;
  }

  const { agents, summary } = response;
  const problemAnalysis = agents.problem_analysis?.data;
  const resources = agents.resources?.data?.resources || [];
  const explanation = agents.explanation?.data?.explanation;
  const guidance = agents.guidance?.data?.guidance;
  const practice = agents.practice?.data?.problems || [];

  const handleDownloadPDF = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/download-questions-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          concept: summary?.concept,
          difficulty_level: summary?.difficulty_level,
          questions: practice
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate PDF');
      }

      // Get the PDF as a blob
      const blob = await response.blob();
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${summary?.concept.replace(/\s+/g, '_')}_questions.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading PDF:', err);
      alert('Failed to download PDF. Please try again.');
    }
  };

  return (
    <div className="response-display">
      <div className="response-header">
        <h2>📚 Learning Guidance for: {summary?.concept}</h2>
        <p>Level: <strong>{summary?.difficulty_level}</strong></p>
      </div>

      <div className="tabs">
        <button
          className={`tab-button ${activeTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analysis')}
        >
          📊 Problem Analysis
        </button>
        <button
          className={`tab-button ${activeTab === 'resources' ? 'active' : ''}`}
          onClick={() => setActiveTab('resources')}
        >
          🔗 Resources ({resources.length})
        </button>
        <button
          className={`tab-button ${activeTab === 'explanation' ? 'active' : ''}`}
          onClick={() => setActiveTab('explanation')}
        >
          💡 Explanation
        </button>
        <button
          className={`tab-button ${activeTab === 'guidance' ? 'active' : ''}`}
          onClick={() => setActiveTab('guidance')}
        >
          🗺️ Guidance
        </button>
        <button
          className={`tab-button ${activeTab === 'practice' ? 'active' : ''}`}
          onClick={() => setActiveTab('practice')}
        >
          📝 Questions ({practice.length})
        </button>
      </div>

      <div className="tab-content">
        {/* Problem Analysis Tab */}
        {activeTab === 'analysis' && problemAnalysis && (
          <div className="tab-panel">
            <h3>Understanding Your Problem</h3>
            <div className="analysis-grid">
              <div className="analysis-card">
                <h4>Main Concept</h4>
                <p>{problemAnalysis.concept}</p>
              </div>
              <div className="analysis-card">
                <h4>You're Stuck At</h4>
                <p>{problemAnalysis.stuck_at}</p>
              </div>
              <div className="analysis-card">
                <h4>Difficulty Level</h4>
                <p className="badge">{problemAnalysis.difficulty_level}</p>
              </div>
              <div className="analysis-card">
                <h4>Your Learning Style</h4>
                <p className="badge">{problemAnalysis.learning_style_hint}</p>
              </div>
            </div>

            <div className="analysis-section">
              <h4>Sub-Concepts to Learn</h4>
              <ul className="concepts-list">
                {problemAnalysis.subconcepts?.map((concept, idx) => (
                  <li key={idx}>{concept}</li>
                ))}
              </ul>
            </div>

            <div className="analysis-section">
              <h4>Common Misconceptions</h4>
              <ul className="misconceptions-list">
                {problemAnalysis.misconceptions?.map((misconception, idx) => (
                  <li key={idx}>{misconception}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Resources Tab */}
        {activeTab === 'resources' && (
          <div className="tab-panel">
            <h3>Recommended Learning Resources</h3>
            <div className="resources-grid">
              {resources.map((resource, idx) => (
                <div
                  key={idx}
                  onClick={() => window.open(resource.url, '_blank')}
                  className="resource-card"
                  style={{ cursor: 'pointer' }}
                >
                  <div className="resource-icon">{resource.icon}</div>
                  <h4>{resource.title}</h4>
                  <p>{resource.description}</p>
                  <span className="resource-type">{resource.type}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Explanation Tab */}
{activeTab === 'explanation' && explanation && (
  <div className="tab-panel">
    <h3>📖 Deep Explanation</h3>
    
    {(() => {
      try {
        let data = explanation;
        
        // Parse if it's a string
        if (typeof data === 'string') {
          data = JSON.parse(data);
        }
        
        // If still not an object, show error
        if (typeof data !== 'object' || data === null) {
          return <p>Could not parse explanation</p>;
        }
        
        return (
          <div className="deep-explanation">
            {/* Overview */}
            {data.overview && (
              <section className="explanation-section">
                <h4>Overview</h4>
                <p className="overview-text">{data.overview}</p>
              </section>
            )}
            
            {/* History */}
            {data.history && (
              <section className="explanation-section">
                <h4>📜 History & Origin</h4>
                <div className="history-box">
                  {data.history.created_when && (
                    <div className="history-item">
                      <strong>When:</strong> {data.history.created_when}
                    </div>
                  )}
                  {data.history.created_by && (
                    <div className="history-item">
                      <strong>Created by:</strong> {data.history.created_by}
                    </div>
                  )}
                  {data.history.why_created && (
                    <div className="history-item">
                      <strong>Why it was created:</strong> {data.history.why_created}
                    </div>
                  )}
                  {data.history.evolution && (
                    <div className="history-item">
                      <strong>Evolution:</strong> {data.history.evolution}
                    </div>
                  )}
                </div>
              </section>
            )}
            
            {/* Core Principles */}
            {data.core_principles && data.core_principles.length > 0 && (
              <section className="explanation-section">
                <h4>🎯 Core Principles</h4>
                <ul className="principles-list">
                  {data.core_principles.map((principle, idx) => (
                    <li key={idx}>{principle}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Step by Step */}
            {data.step_by_step_breakdown && data.step_by_step_breakdown.length > 0 && (
              <section className="explanation-section">
                <h4>📋 Step-by-Step Breakdown</h4>
                <div className="steps-list">
                  {data.step_by_step_breakdown.map((step, idx) => (
                    <div key={idx} className="step-item">
                      {step}
                    </div>
                  ))}
                </div>
              </section>
            )}
            
            {/* Real-World Applications */}
            {data.real_world_applications && data.real_world_applications.length > 0 && (
              <section className="explanation-section">
                <h4>🌍 Real-World Applications</h4>
                <ul className="applications-list">
                  {data.real_world_applications.map((app, idx) => (
                    <li key={idx}>{app}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Key Concepts */}
            {data.key_concepts && data.key_concepts.length > 0 && (
              <section className="explanation-section">
                <h4>🔑 Key Concepts</h4>
                <ul className="concepts-list">
                  {data.key_concepts.map((concept, idx) => (
                    <li key={idx}>{concept}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Analogies */}
            {data.analogies && data.analogies.length > 0 && (
              <section className="explanation-section">
                <h4>💡 Real-World Analogies</h4>
                <div className="analogies-box">
                  {data.analogies.map((analogy, idx) => (
                    <div key={idx} className="analogy-item">
                      {analogy}
                    </div>
                  ))}
                </div>
              </section>
            )}
            
            {/* Advantages */}
            {data.advantages && data.advantages.length > 0 && (
              <section className="explanation-section">
                <h4>✅ Advantages</h4>
                <ul className="advantages-list">
                  {data.advantages.map((adv, idx) => (
                    <li key={idx}>{adv}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Limitations */}
            {data.limitations && data.limitations.length > 0 && (
              <section className="explanation-section">
                <h4>⚠️ Limitations</h4>
                <ul className="limitations-list">
                  {data.limitations.map((lim, idx) => (
                    <li key={idx}>{lim}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Comparisons */}
            {data.comparisons && Object.keys(data.comparisons).length > 0 && (
              <section className="explanation-section">
                <h4>🔄 Comparisons</h4>
                <div className="comparisons-box">
                  {Object.entries(data.comparisons).map(([key, value]) => (
                    <div key={key} className="comparison-item">
                      <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                    </div>
                  ))}
                </div>
              </section>
            )}
            
            {/* Best Practices */}
            {data.best_practices && data.best_practices.length > 0 && (
              <section className="explanation-section">
                <h4>🏆 Best Practices</h4>
                <ul className="best-practices-list">
                  {data.best_practices.map((practice, idx) => (
                    <li key={idx}>{practice}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Common Mistakes */}
            {data.common_mistakes && data.common_mistakes.length > 0 && (
              <section className="explanation-section">
                <h4>❌ Common Mistakes</h4>
                <ul className="mistakes-list">
                  {data.common_mistakes.map((mistake, idx) => (
                    <li key={idx}>{mistake}</li>
                  ))}
                </ul>
              </section>
            )}
            
            {/* Why It Matters */}
            {data.why_it_matters && (
              <section className="explanation-section important">
                <h4>⭐ Why It Matters</h4>
                <p>{data.why_it_matters}</p>
              </section>
            )}
          </div>
        );
      } catch (error) {
        console.error('Explanation parse error:', error);
        return <p>Could not display explanation</p>;
      }
    })()}
  </div>
)}
       {/* Guidance Tab */}
{activeTab === 'guidance' && guidance && (
  <div className="tab-panel">
    <h3>🗺️ Step-by-Step Guidance</h3>
    
    {(() => {
      try {
        let data = guidance;
        
        // Parse if string
        if (typeof data === 'string') {
          data = JSON.parse(data);
        }
        
        // Get steps
        const steps = data?.steps || [];
        const encouragement = data?.encouragement || '';
        
        // Check if we have steps
        if (steps && steps.length > 0) {
          return (
            <div className="guidance-steps">
              {steps.map((step, idx) => (
                <div key={idx} className="guidance-step">
                  <div className="step-header">
                    <div className="step-number">{step.step_number || idx + 1}</div>
                    <div className="step-info">
                      <h4>{step.title}</h4>
                    </div>
                  </div>
                  
                  <div className="step-content">
                    <p className="step-description">{step.description}</p>
                    
                    {step.hint && (
                      <div className="step-hint">
                        <strong>💡 Hint:</strong> {step.hint}
                      </div>
                    )}
                    
                    {step.thinking_question && (
                      <div className="step-question">
                        <strong>🤔 Think about:</strong> {step.thinking_question}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {encouragement && (
                <div className="encouragement-box">
                  <p>💪 {encouragement}</p>
                </div>
              )}
            </div>
          );
        }
        
        // Fallback
        return <p>No guidance steps available</p>;
      } catch (error) {
        console.error('Guidance error:', error);
        return <p>Could not parse guidance</p>;
      }
    })()}
  </div>
)}
        {/* Questions Tab - Study Material */}
        {activeTab === 'practice' && (
          <div className="tab-panel">
            <div className="questions-header">
              <h3>📚 Study Questions ({practice.length})</h3>
              <button 
                className="download-pdf-btn"
                onClick={() => handleDownloadPDF()}
              >
                ⬇️ Download as PDF
              </button>
            </div>

            {practice.length === 0 ? (
              <p>No study questions available yet.</p>
            ) : (
              <div className="questions-list">
                {practice.map((question, idx) => (
                  <div key={idx} className="question-card">
                    <div className="question-header">
                      <div className="question-number">Q{question.question_number || idx + 1}</div>
                      <div className="question-info">
                        <span className="importance-badge">
                          {question.importance || '⭐ Important'}
                        </span>
                        <span className={`difficulty-badge ${question.difficulty || 'beginner'}`}>
                          {question.difficulty || 'beginner'}
                        </span>
                      </div>
                    </div>

                    <p className="question-text">{question.question}</p>

                    <details className="answer-details">
                      <summary>📖 View Answer & Explanation</summary>
                      <div className="answer-section">
                        <div className="answer-box">
                          <strong>Answer:</strong>
                          <p>{question.answer}</p>
                        </div>
                        <div className="explanation-box">
                          <strong>Explanation:</strong>
                          <p>{question.explanation}</p>
                        </div>
                      </div>
                    </details>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResponseDisplay;