import type { Problem } from '../types';
import DifficultyBadge from './DifficultyBadge';
import HighlightedText from './HighlightedText';

interface ProblemListProps {
  problems: Problem[];
  selectedProblemId?: string;
  onSelectProblem: (problemId: string) => void;
}

function ProblemList({ problems, selectedProblemId, onSelectProblem }: ProblemListProps) {
  if (!problems || problems.length === 0) {
    return (
      <div className="p-4 text-gray-500 text-sm">
        No problems found
      </div>
    );
  }

  return (
    <div className="divide-y divide-gray-700">
      {problems.map((problem) => {
        const isSelected = problem.problem_id === selectedProblemId;
        return (
          <button
            key={problem.problem_id}
            onClick={() => onSelectProblem(problem.problem_id)}
            className={`w-full text-left p-4 transition-colors ${
              isSelected
                ? 'bg-blue-900/30 border-l-4 border-blue-500'
                : 'hover:bg-gray-800 border-l-4 border-transparent'
            }`}
          >
          <div className="flex items-start justify-between gap-2 mb-1">
            <h3 className="font-medium text-gray-200 text-sm">
              {problem.highlight?.title ? (
                <HighlightedText text={problem.highlight.title} />
              ) : (
                problem.title
              )}
            </h3>
            <DifficultyBadge difficulty={problem.difficulty} />
          </div>
          {problem.topics && problem.topics.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {problem.topics.slice(0, 3).map((topic) => (
                <span
                  key={topic}
                  className="text-xs text-gray-400 bg-gray-700 px-2 py-0.5 rounded"
                >
                  {topic}
                </span>
              ))}
              {problem.topics.length > 3 && (
                <span className="text-xs text-gray-500">
                  +{problem.topics.length - 3}
                </span>
              )}
            </div>
          )}
          </button>
        );
      })}
    </div>
  );
}

export default ProblemList;
