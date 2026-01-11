// API Types

export type Difficulty = 'Easy' | 'Medium' | 'Hard';

export interface SearchHighlight {
  title: string;
  topics?: string | null;
}

export interface Problem {
  problem_id: string;
  title: string;
  difficulty?: Difficulty;
  topics?: string[];
  leetcode_url: string;
  score?: number;
  highlight?: SearchHighlight | null;
}

export interface Solution {
  approach: string;
  time_complexity: string;
  space_complexity: string;
  explanation: string;
  code: string;
}

export interface SimilarProblem {
  title: string;
  url: string;
}

export interface ProblemDetail extends Problem {
  solutions: Solution[];
  key_insights?: string[];
  edge_cases?: string[];
  similar_problems?: SimilarProblem[];
}

export interface Stats {
  total_problems: number;
  total_solutions: number;
  by_difficulty?: {
    Easy?: number;
    Medium?: number;
    Hard?: number;
  };
}

export interface GetProblemsParams {
  difficulty?: Difficulty;
  topic?: string;
  limit?: number;
  offset?: number;
}
