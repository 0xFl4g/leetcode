import { useState } from 'react';
import type { ProblemDetail } from '../types';
import DifficultyBadge from './DifficultyBadge';
import CodeBlock from './CodeBlock';

interface CollapsibleSectionProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

function CollapsibleSection({ title, children, defaultOpen = false }: CollapsibleSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-gray-700 rounded-lg overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 bg-gray-800 hover:bg-gray-750 flex items-center justify-between transition-colors"
      >
        <span className="font-medium text-gray-200">{title}</span>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {isOpen && (
        <div className="p-4 bg-gray-900">
          {children}
        </div>
      )}
    </div>
  );
}

interface SolutionDisplayProps {
  solution: ProblemDetail | null;
}

function SolutionDisplay({ solution }: SolutionDisplayProps) {
  if (!solution) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Select a problem to view solutions
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <h1 className="text-3xl font-bold text-white">{solution.title}</h1>
          <DifficultyBadge difficulty={solution.difficulty} />
        </div>
        {solution.topics && solution.topics.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {solution.topics.map((topic) => (
              <span
                key={topic}
                className="text-sm bg-blue-900/50 text-blue-300 px-3 py-1 rounded-full"
              >
                {topic}
              </span>
            ))}
          </div>
        )}
        <a
          href={solution.leetcode_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:text-blue-300 text-sm"
        >
          View on LeetCode →
        </a>
      </div>

      {/* Solutions */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">Solutions</h2>
        <div className="space-y-4">
          {solution.solutions.map((sol, index) => (
            <div key={index} className="border border-gray-700 rounded-lg p-6 bg-gray-800/50">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                  {sol.approach}
                </h3>
                <div className="flex gap-4 text-sm">
                  <span className="text-gray-400">
                    Time: <span className="font-mono font-medium text-green-400">{sol.time_complexity}</span>
                  </span>
                  <span className="text-gray-400">
                    Space: <span className="font-mono font-medium text-blue-400">{sol.space_complexity}</span>
                  </span>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-200 mb-2">Explanation</h4>
                  <p className="text-gray-400 leading-relaxed">{sol.explanation}</p>
                </div>

                <CollapsibleSection title="Code" defaultOpen={false}>
                  <CodeBlock code={sol.code} />
                </CollapsibleSection>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Key Insights */}
      {solution.key_insights && solution.key_insights.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-white mb-3">Key Insights</h2>
          <ul className="space-y-2">
            {solution.key_insights.map((insight, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span className="text-gray-300">{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Edge Cases */}
      {solution.edge_cases && solution.edge_cases.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-white mb-3">Edge Cases</h2>
          <ul className="space-y-2">
            {solution.edge_cases.map((edgeCase, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-yellow-400 mt-1">⚠</span>
                <span className="text-gray-300">{edgeCase}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Similar Problems */}
      {solution.similar_problems && solution.similar_problems.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-white mb-3">Similar Problems</h2>
          <ul className="space-y-2">
            {solution.similar_problems.map((problem, index) => (
              <li key={index}>
                <a
                  href={problem.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300"
                >
                  {problem.title} →
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default SolutionDisplay;
