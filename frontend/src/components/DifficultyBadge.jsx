import React from 'react';

const DIFFICULTY_STYLES = {
  Easy: 'bg-green-100 text-green-800',
  Medium: 'bg-yellow-100 text-yellow-800',
  Hard: 'bg-red-100 text-red-800',
};

function DifficultyBadge({ difficulty }) {
  const styles = DIFFICULTY_STYLES[difficulty] || 'bg-gray-100 text-gray-800';

  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded ${styles}`}>
      {difficulty}
    </span>
  );
}

export default DifficultyBadge;
