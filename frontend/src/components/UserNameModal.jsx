/**
 * UserNameModal Component
 * Asks for user's name on first visit
 */

import React, { useState } from 'react';
import './UserNameModal.css';

function UserNameModal({ onSave }) {
  const [name, setName] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      localStorage.setItem('userName', name);
      setSubmitted(true);
      onSave(name);
    }
  };

  if (submitted) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <div className="modal-icon">👋</div>
        <h2>Welcome to Guided Learning AI!</h2>
        <p>What's your name?</p>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoFocus
            maxLength="50"
          />
          <button type="submit" disabled={!name.trim()}>
            Let's Learn! 🚀
          </button>
        </form>
      </div>
    </div>
  );
}

export default UserNameModal;