type CardColor = 'default' | 'green' | 'yellow' | 'red';

const colorClasses: Record<CardColor, string> = {
  default: 'bg-gray-800 border-gray-700 hover:bg-gray-750',
  green: 'bg-green-900/30 border-green-700 hover:bg-green-900/50',
  yellow: 'bg-yellow-900/30 border-yellow-700 hover:bg-yellow-900/50',
  red: 'bg-red-900/30 border-red-700 hover:bg-red-900/50',
};

interface StatsCardProps {
  label: string;
  value: number | string;
  color?: CardColor;
  onClick?: () => void;
}

function StatsCard({ label, value, color = 'default', onClick }: StatsCardProps) {
  const baseClasses = 'p-4 rounded-lg border transition-colors';
  const colorClass = colorClasses[color] || colorClasses.default;
  const clickableClass = onClick ? 'cursor-pointer' : '';

  return (
    <div
      className={`${baseClasses} ${colorClass} ${clickableClass}`}
      onClick={onClick}
    >
      <div className="text-2xl font-bold text-white">
        {typeof value === 'number' ? value.toLocaleString() : value}
      </div>
      <div className="text-sm text-gray-400">{label}</div>
    </div>
  );
}

export default StatsCard;
