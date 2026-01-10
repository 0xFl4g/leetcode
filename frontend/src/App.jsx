import React, { useState, useEffect } from 'react';
import ProblemList from './components/ProblemList';
import SolutionDisplay from './components/SolutionDisplay';
import { getAllProblems, getProblemById, searchProblems } from './services/api';

function App() {
  const [problems, setProblems] = useState([]);
  const [filteredProblems, setFilteredProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [selectedProblemId, setSelectedProblemId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [difficultyFilter, setDifficultyFilter] = useState('');

  // Load all problems on mount
  useEffect(() => {
    loadProblems();
  }, []);

  // Filter problems when search query or difficulty changes
  useEffect(() => {
    if (searchQuery) {
      handleSearch();
    } else if (difficultyFilter) {
      loadProblems({ difficulty: difficultyFilter });
    } else {
      setFilteredProblems(problems);
    }
  }, [searchQuery, difficultyFilter]);

  const loadProblems = async (filters = {}) => {
    try {
      setLoading(true);
      const data = await getAllProblems(filters);
      setProblems(data);
      setFilteredProblems(data);
      setError(null);
    } catch (err) {
      setError('Failed to load problems');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setFilteredProblems(problems);
      return;
    }

    try {
      const results = await searchProblems(searchQuery);
      setFilteredProblems(results);
    } catch (err) {
      console.error('Search failed:', err);
    }
  };

  const handleSelectProblem = async (problemId) => {
    try {
      setSelectedProblemId(problemId);
      const solution = await getProblemById(problemId);
      setSelectedProblem(solution);
    } catch (err) {
      setError('Failed to load problem details');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            LeetCode Learning Tool
          </h1>

          {/* Search Bar */}
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Search problems..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            {/* Difficulty Filter */}
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <div className="text-gray-500">Loading problems...</div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Sidebar - Problem List */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm overflow-hidden sticky top-24">
                <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                  <h2 className="font-semibold text-gray-900">
                    Problems ({filteredProblems.length})
                  </h2>
                </div>
                <div className="max-h-[calc(100vh-200px)] overflow-y-auto">
                  <ProblemList
                    problems={filteredProblems}
                    selectedProblemId={selectedProblemId}
                    onSelectProblem={handleSelectProblem}
                  />
                </div>
              </div>
            </div>

            {/* Main Content - Solution Display */}
            <div className="lg:col-span-3">
              <div className="bg-white rounded-lg shadow-sm p-6">
                <SolutionDisplay solution={selectedProblem} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
