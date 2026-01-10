import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Get all problems with optional filtering
 */
export const getAllProblems = async (filters = {}) => {
  const params = new URLSearchParams();

  if (filters.difficulty) {
    params.append('difficulty', filters.difficulty);
  }
  if (filters.topic) {
    params.append('topic', filters.topic);
  }

  const response = await api.get('/problems', { params });
  return response.data;
};

/**
 * Get full solution for a specific problem
 */
export const getProblemById = async (problemId) => {
  const response = await api.get(`/problems/${problemId}`);
  return response.data;
};

/**
 * Search problems by query string
 */
export const searchProblems = async (query) => {
  const response = await api.get('/search', {
    params: { q: query },
  });
  return response.data;
};

/**
 * Get problem by LeetCode URL
 */
export const getProblemByUrl = async (url) => {
  const response = await api.get('/problems/by-url', {
    params: { url },
  });
  return response.data;
};

export default api;
