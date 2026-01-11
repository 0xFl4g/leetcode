import type { Stats, Problem, ProblemDetail, GetProblemsParams } from '../types';

const API_BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

/**
 * Get database statistics
 */
export const getStats = (): Promise<Stats> => fetchAPI<Stats>('/stats');

/**
 * Get all problems with optional filtering and pagination
 */
export const getAllProblems = async ({
  difficulty,
  topic,
  limit = 50,
  offset = 0,
}: GetProblemsParams = {}): Promise<Problem[]> => {
  const params = new URLSearchParams();
  if (difficulty) params.append('difficulty', difficulty);
  if (topic) params.append('topic', topic);
  params.append('limit', String(limit));
  params.append('offset', String(offset));
  return fetchAPI<Problem[]>(`/problems?${params}`);
};

/**
 * Get full solution for a specific problem
 */
export const getProblemById = (problemId: string): Promise<ProblemDetail> =>
  fetchAPI<ProblemDetail>(`/problems/${problemId}`);

/**
 * Search problems by query string
 */
export const searchProblems = (query: string): Promise<Problem[]> =>
  fetchAPI<Problem[]>(`/search?q=${encodeURIComponent(query)}`);

/**
 * Get problem by LeetCode URL
 */
export const getProblemByUrl = (url: string): Promise<ProblemDetail> =>
  fetchAPI<ProblemDetail>(`/problems/by-url?url=${encodeURIComponent(url)}`);
