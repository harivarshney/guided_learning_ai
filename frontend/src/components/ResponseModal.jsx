/**
 * ResponseModal Component
 * Displays full learning response in a modal overlay
 */

import React from 'react';
import ResponseDisplay from './ResponseDisplay';
import './ResponseModal.css';

function ResponseModal({ response, onClose }) {
  if (!response) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>📚 Previous Learning Session</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>
        
        <div className="modal-body">
          <ResponseDisplay response={response} />
        </div>
      </div>
    </div>
  );
}

export default ResponseModal;