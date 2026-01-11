import { useState, useEffect } from 'react';
import { Routes, Route, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import ProblemList from './components/ProblemList';
import SolutionDisplay from './components/SolutionDisplay';
import StatsCard from './components/StatsCard';
import { getAllProblems, getProblemById, searchProblems, getStats } from './services/api';
import { useDebounce } from './hooks/useDebounce';
import type { Stats, Problem, ProblemDetail, Difficulty } from './types';

const PROBLEMS_PER_PAGE = 50;

interface HeaderProps {
  stats: Stats | null;
}

function Header({ stats }: HeaderProps) {
  const navigate = useNavigate();

  return (
    <header className="bg-gray-900 sticky top-0 z-10 border-b border-gray-700">
      <div className="px-4 py-3 flex items-center justify-between">
        <button
          onClick={() => navigate('/')}
          className="text-xl font-bold text-white hover:text-blue-400 transition-colors"
        >
          LeetCode Solutions
        </button>
        {stats && (
          <p className="text-sm text-gray-400">
            {stats.total_problems.toLocaleString()} problems · {stats.total_solutions.toLocaleString()} solutions
          </p>
        )}
      </div>
    </header>
  );
}

function MasterDetailLayout() {
  const navigate = useNavigate();
  const { problemId } = useParams<{ problemId: string }>();
  const [searchParams, setSearchParams] = useSearchParams();

  const [stats, setStats] = useState<Stats | null>(null);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);

  // Detail panel state
  const [solution, setSolution] = useState<ProblemDetail | null>(null);
  const [loadingSolution, setLoadingSolution] = useState(false);
  const [solutionError, setSolutionError] = useState<string | null>(null);

  const searchQuery = searchParams.get('q') || '';
  const difficultyFilter = (searchParams.get('difficulty') || '') as Difficulty | '';

  // Local state for search input (for debouncing)
  const [searchInput, setSearchInput] = useState(searchQuery);
  const debouncedSearch = useDebounce(searchInput, 300);

  // Update URL when debounced search changes
  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    if (debouncedSearch) params.set('q', debouncedSearch);
    else params.delete('q');

    // Only update if the value actually changed
    if (params.get('q') !== searchParams.get('q')) {
      setSearchParams(params);
    }
  }, [debouncedSearch]);

  // Sync local input when URL changes externally (e.g., browser back/forward)
  useEffect(() => {
    setSearchInput(searchQuery);
  }, [searchQuery]);

  // Load stats on mount
  useEffect(() => {
    getStats().then(setStats).catch(console.error);
  }, []);

  // Load problems when filters change
  useEffect(() => {
    setOffset(0);
    setProblems([]);
    setHasMore(true);
    loadProblems(0, true);
  }, [searchQuery, difficultyFilter]);

  // Load solution when problemId changes
  useEffect(() => {
    if (!problemId) {
      setSolution(null);
      return;
    }

    setLoadingSolution(true);
    setSolutionError(null);
    getProblemById(problemId)
      .then(setSolution)
      .catch((err) => {
        setSolutionError('Problem not found');
        console.error(err);
      })
      .finally(() => setLoadingSolution(false));
  }, [problemId]);

  const loadProblems = async (currentOffset = 0, reset = false) => {
    try {
      if (reset) setLoading(true);
      else setLoadingMore(true);

      let data: Problem[];
      if (searchQuery) {
        data = await searchProblems(searchQuery);
        setHasMore(false);
      } else {
        data = await getAllProblems({
          difficulty: difficultyFilter || undefined,
          limit: PROBLEMS_PER_PAGE,
          offset: currentOffset,
        });
        setHasMore(data.length === PROBLEMS_PER_PAGE);
      }

      if (reset) {
        setProblems(data);
      } else {
        setProblems(prev => [...prev, ...data]);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load problems');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const loadMore = () => {
    const newOffset = offset + PROBLEMS_PER_PAGE;
    setOffset(newOffset);
    loadProblems(newOffset, false);
  };

  const handleDifficultyChange = (difficulty: string) => {
    const params = new URLSearchParams(searchParams);
    if (difficulty) params.set('difficulty', difficulty);
    else params.delete('difficulty');
    params.delete('q');
    setSearchParams(params);
  };

  const handleSelectProblem = (id: string) => {
    // Preserve search params when navigating
    const params = searchParams.toString();
    navigate(`/problems/${id}${params ? `?${params}` : ''}`);
  };

  const handleCloseSolution = () => {
    const params = searchParams.toString();
    navigate(`/${params ? `?${params}` : ''}`);
  };

  const handleExpandToFullPage = () => {
    navigate(`/problems/${problemId}/full`);
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
      <Header stats={stats} />

      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Problem List */}
        <div className="w-96 bg-gray-900 border-r border-gray-700 flex flex-col shrink-0">

          {/* Search and Filters */}
          <div className="p-3 border-b border-gray-700 flex gap-2">
            <input
              type="text"
              placeholder="Search..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              className="flex-1 px-3 py-1.5 text-sm bg-gray-800 border border-gray-600 rounded text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
              value={difficultyFilter}
              onChange={(e) => handleDifficultyChange(e.target.value)}
              className="px-2 py-1.5 text-sm bg-gray-800 border border-gray-600 rounded text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          {error && (
            <div className="p-3 bg-red-900/50 text-red-300 text-sm">
              {error}
            </div>
          )}

          {/* Problem List */}
          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="p-8 text-center text-gray-500">Loading...</div>
            ) : (
              <>
                <ProblemList
                  problems={problems}
                  selectedProblemId={problemId}
                  onSelectProblem={handleSelectProblem}
                />
                {hasMore && !searchQuery && (
                  <div className="p-3 border-t border-gray-700">
                    <button
                      onClick={loadMore}
                      disabled={loadingMore}
                      className="w-full py-2 text-sm text-blue-400 hover:bg-gray-800 rounded disabled:opacity-50"
                    >
                      {loadingMore ? 'Loading...' : `Load More (${problems.length}+)`}
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {/* Right Panel - Solution Detail */}
        <div className="flex-1 flex flex-col overflow-hidden bg-gray-950">
          {problemId ? (
            <>
              {/* Detail Header */}
              <div className="px-4 py-3 border-b border-gray-700 flex items-center justify-between bg-gray-900">
                <button
                  onClick={handleCloseSolution}
                  className="text-gray-400 hover:text-gray-200 flex items-center gap-1 text-sm"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Close
                </button>
                <button
                  onClick={handleExpandToFullPage}
                  className="text-gray-400 hover:text-gray-200 flex items-center gap-1 text-sm"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                  Full Page
                </button>
              </div>

              {/* Detail Content */}
              <div className="flex-1 overflow-y-auto p-6">
                {solutionError && (
                  <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
                    {solutionError}
                  </div>
                )}

                {loadingSolution ? (
                  <div className="text-center py-12 text-gray-500">Loading solution...</div>
                ) : (
                  <SolutionDisplay solution={solution} />
                )}
              </div>
            </>
          ) : (
            /* Home page when no problem selected */
            <div className="flex-1 overflow-y-auto p-8">
              <div className="max-w-2xl mx-auto">
                {/* Hero Section */}
                <div className="text-center mb-10">
                  <h1 className="text-4xl font-bold text-white mb-4">
                    LeetCode Solutions
                  </h1>
                  <p className="text-lg text-gray-400">
                    A curated collection of LeetCode problem solutions with detailed explanations,
                    time/space complexity analysis, and multiple approaches.
                  </p>
                </div>

                {/* Stats Grid */}
                {stats && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                    <StatsCard label="Total Problems" value={stats.total_problems} />
                    <StatsCard
                      label="Easy"
                      value={stats.by_difficulty?.Easy || 0}
                      color="green"
                      onClick={() => handleDifficultyChange('Easy')}
                    />
                    <StatsCard
                      label="Medium"
                      value={stats.by_difficulty?.Medium || 0}
                      color="yellow"
                      onClick={() => handleDifficultyChange('Medium')}
                    />
                    <StatsCard
                      label="Hard"
                      value={stats.by_difficulty?.Hard || 0}
                      color="red"
                      onClick={() => handleDifficultyChange('Hard')}
                    />
                  </div>
                )}

                {/* Features */}
                <div className="grid md:grid-cols-3 gap-6 mb-10">
                  <div className="bg-gray-800 rounded-lg p-5">
                    <div className="w-10 h-10 bg-blue-900/50 rounded-lg flex items-center justify-center mb-3">
                      <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                      </svg>
                    </div>
                    <h3 className="font-semibold text-white mb-1">Multiple Approaches</h3>
                    <p className="text-sm text-gray-400">Each problem includes various solution approaches from brute force to optimal.</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-5">
                    <div className="w-10 h-10 bg-green-900/50 rounded-lg flex items-center justify-center mb-3">
                      <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <h3 className="font-semibold text-white mb-1">Complexity Analysis</h3>
                    <p className="text-sm text-gray-400">Time and space complexity provided for every solution approach.</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-5">
                    <div className="w-10 h-10 bg-purple-900/50 rounded-lg flex items-center justify-center mb-3">
                      <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <h3 className="font-semibold text-white mb-1">Syntax Highlighting</h3>
                    <p className="text-sm text-gray-400">Clean, readable code with syntax highlighting and one-click copy.</p>
                  </div>
                </div>

                {/* Getting Started */}
                <div className="bg-blue-900/30 border border-blue-800 rounded-lg p-6 text-center">
                  <h3 className="font-semibold text-blue-300 mb-2">Get Started</h3>
                  <p className="text-blue-400 text-sm">
                    Select a problem from the list on the left, or use the search bar to find specific problems by name or topic.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function FullPageView() {
  const { problemId } = useParams<{ problemId: string }>();
  const navigate = useNavigate();
  const [stats, setStats] = useState<Stats | null>(null);
  const [solution, setSolution] = useState<ProblemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getStats().then(setStats).catch(console.error);
  }, []);

  useEffect(() => {
    if (!problemId) return;

    setLoading(true);
    getProblemById(problemId)
      .then(setSolution)
      .catch((err) => {
        setError('Problem not found');
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, [problemId]);

  const handleBack = () => {
    navigate(`/problems/${problemId}`);
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
      <Header stats={stats} />

      <div className="flex-1 max-w-5xl mx-auto w-full px-4 py-6">
        <button
          onClick={handleBack}
          className="mb-4 text-blue-400 hover:text-blue-300 flex items-center gap-1 text-sm"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to split view
        </button>

        {error && (
          <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12 text-gray-500">Loading solution...</div>
        ) : (
          <div className="bg-gray-900 rounded-lg shadow-sm p-6">
            <SolutionDisplay solution={solution} />
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<MasterDetailLayout />} />
      <Route path="/problems/:problemId" element={<MasterDetailLayout />} />
      <Route path="/problems/:problemId/full" element={<FullPageView />} />
    </Routes>
  );
}

export default App;
