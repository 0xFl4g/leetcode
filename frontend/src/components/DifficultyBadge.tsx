import type { Difficulty } from '../types';

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  Easy: 'bg-green-900/50 text-green-400',
  Medium: 'bg-yellow-900/50 text-yellow-400',
  Hard: 'bg-red-900/50 text-red-400',
};

interface DifficultyBadgeProps {
  difficulty?: Difficulty;
}

function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  if (!difficulty) {
    return null;
  }

  const styles = DIFFICULTY_STYLES[difficulty] || 'bg-gray-700 text-gray-400';

  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded ${styles}`}>
      {difficulty}
    </span>
  );
}

export default DifficultyBadge;
