/**
 * API Client
 * Connects frontend to backend at http://localhost:8000
 */

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const askQuestion = async (question, userId) => {
  try {
    const response = await client.post('/ask', {
      question,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    console.error('Error asking question:', error);
    throw error;
  }
};

export const getUserHistory = async (userId) => {
  try {
    const response = await client.get(`/user/${userId}/history`);
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export const getUserProgress = async (userId) => {
  try {
    const response = await client.get(`/user/${userId}/progress`);
    return response.data;
  } catch (error) {
    console.error('Error fetching progress:', error);
    throw error;
  }
};

export const getConceptQuestions = async (concept) => {
  try {
    const response = await client.get(`/concept/${concept}/questions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching concept questions:', error);
    throw error;
  }
};

/**
 * Check practice answer
 * Sends answer to backend for evaluation
 */
export async function checkPracticeAnswer(data) {
  try {
    const response = await fetch(`${API_URL}/check-practice-answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Backend error:', errorText);
      throw new Error(`Backend error: ${response.status}`);
    }

    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to check answer');
    }

    return result;
  } catch (err) {
    console.error('Error checking answer:', err);
    throw err;
  }
}

export default client;