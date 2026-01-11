/**
 * Renders text with <mark> tags as highlighted spans.
 * Safe alternative that parses the string and renders React elements.
 */

interface HighlightedTextProps {
  text: string;
  className?: string;
}

function HighlightedText({ text, className = '' }: HighlightedTextProps) {
  // Parse text and extract mark tags safely
  const parts: { text: string; isHighlight: boolean }[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    const markStart = remaining.indexOf('<mark>');

    if (markStart === -1) {
      if (remaining) {
        parts.push({ text: remaining, isHighlight: false });
      }
      break;
    }

    if (markStart > 0) {
      parts.push({ text: remaining.slice(0, markStart), isHighlight: false });
    }

    const markEnd = remaining.indexOf('</mark>', markStart);
    if (markEnd === -1) {
      parts.push({ text: remaining.slice(markStart), isHighlight: false });
      break;
    }

    const highlightedText = remaining.slice(markStart + 6, markEnd);
    parts.push({ text: highlightedText, isHighlight: true });

    remaining = remaining.slice(markEnd + 7);
  }

  return (
    <span className={className}>
      {parts.map((part, i) =>
        part.isHighlight ? (
          <mark
            key={i}
            className="bg-yellow-500/30 text-yellow-200 rounded px-0.5"
          >
            {part.text}
          </mark>
        ) : (
          <span key={i}>{part.text}</span>
        )
      )}
    </span>
  );
}

export default HighlightedText;
