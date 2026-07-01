/**
 * Main App Component
 * Routes and layout for the frontend
 */

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar';
import UserNameModal from './components/UserNameModal';
import HomePage from './pages/Home';
import HistoryPage from './pages/HistoryPage';
import ProgressPage from './pages/ProgressPage';
import './App.css';

function App() {
  const [userId, setUserId] = useState(localStorage.getItem('userId') || 'user_' + Math.random().toString(36).substr(2, 9));
  const [userName, setUserName] = useState(localStorage.getItem('userName') || '');

  // Save user ID to localStorage on first load
  useEffect(() => {
    localStorage.setItem('userId', userId);
  }, [userId]);

  const handleUserNameSave = (name) => {
    setUserName(name);
    localStorage.setItem('userName', name);
  };

  return (
    <Router>
      <div className="App">
        {!userName && <UserNameModal onSave={handleUserNameSave} />}
        <Navbar userId={userId} userName={userName} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage userId={userId} userName={userName} />} />
            <Route path="/history" element={<HistoryPage userId={userId} userName={userName} />} />
            <Route path="/progress" element={<ProgressPage userId={userId} userName={userName} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;