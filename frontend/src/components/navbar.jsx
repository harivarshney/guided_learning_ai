/**
 * Navbar Component
 * Navigation bar with links to all pages
 */

import React from 'react';
import { Link } from 'react-router-dom';
import './navbar.css';

function Navbar({ userId, userName }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🧠 Guided Learning AI
        </Link>

        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Ask Question
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/history" className="nav-link">
              History
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/progress" className="nav-link">
              Progress
            </Link>
          </li>
        </ul>

        <div className="user-info">
          <span className="user-badge">👋 Welcome, {userName}</span>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;