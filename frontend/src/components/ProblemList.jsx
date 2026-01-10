import React from 'react';
import DifficultyBadge from './DifficultyBadge';

function ProblemList({ problems, selectedProblemId, onSelectProblem }) {
  if (!problems || problems.length === 0) {
    return (
      <div className="p-4 text-gray-500 text-sm">
        No problems found
      </div>
    );
  }

  return (
    <div className="divide-y divide-gray-200">
      {problems.map((problem) => (
        <button
          key={problem.problem_id}
          onClick={() => onSelectProblem(problem.problem_id)}
          className={`w-full text-left p-4 hover:bg-gray-50 transition-colors ${
            selectedProblemId === problem.problem_id ? 'bg-blue-50' : ''
          }`}
        >
          <div className="flex items-start justify-between gap-2 mb-2">
            <h3 className="font-medium text-gray-900 text-sm">
              {problem.title}
            </h3>
            <DifficultyBadge difficulty={problem.difficulty} />
          </div>
          <div className="flex flex-wrap gap-1">
            {problem.topics.map((topic) => (
              <span
                key={topic}
                className="text-xs text-gray-600 bg-gray-100 px-2 py-0.5 rounded"
              >
                {topic}
              </span>
            ))}
          </div>
        </button>
      ))}
    </div>
  );
}

export default ProblemList;
